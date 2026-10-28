"""Local practice version of the Part 4 LIME exercise.

This uses the available Part 3 student_data.pqt and trains its own model.
It does not reproduce the canonical Part 4 dataset or model from edX.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import tensorflow as tf
import keras
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import lime.lime_tabular


tf.random.set_seed(42)
np.random.seed(42)

part4_dir = Path(__file__).resolve().parent
lecture_dir = part4_dir.parent
data_path = lecture_dir / "part_3" / "student_data.pqt"
weights_path = part4_dir / "local_test_model_weighted.weights.h5"

if not data_path.is_file():
    raise FileNotFoundError(f"Local practice data not found: {data_path}")

df = pd.read_parquet(data_path)
required = {"grade", "certified"}
missing = required.difference(df.columns)
if missing:
    raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

# Create the same four grade buckets used in the exercise.
thresholds = [0.20, 0.70, 0.90]
n_classes_grade = len(thresholds) + 1
df["performance_bucket"] = np.searchsorted(
    thresholds, df["grade"].to_numpy(), side="right"
)
df["certified"] = df["certified"].astype(int)

leakage_cols = [
    "user_uuid",
    "grade",
    "certified",
    "performance_bucket",
    "completed",
    "cert_status",
    "cert_created_date",
    "cert_modified_date",
]
features = df.drop(
    columns=[c for c in leakage_cols if c in df.columns]
).copy()
labels_grade = df["performance_bucket"]
labels_cert = df["certified"]

categorical_features = features.select_dtypes(
    exclude=np.number
).columns.tolist()
numerical_features = features.select_dtypes(
    include=np.number
).columns.tolist()
features[categorical_features] = features[categorical_features].astype(str)

(
    X_train,
    X_test,
    y_train_grade,
    y_test_grade,
    y_train_cert,
    y_test_cert,
) = train_test_split(
    features,
    labels_grade,
    labels_cert,
    test_size=0.2,
    random_state=42,
    stratify=labels_cert,
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            ),
            numerical_features,
        ),
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical_features,
        ),
    ]
)

X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

if sp.issparse(X_train_transformed):
    X_train_transformed = X_train_transformed.toarray()
if sp.issparse(X_test_transformed):
    X_test_transformed = X_test_transformed.toarray()
X_train_transformed = np.asarray(X_train_transformed, dtype=np.float32)
X_test_transformed = np.asarray(X_test_transformed, dtype=np.float32)

y_train = {
    "grade_output": keras.utils.to_categorical(
        y_train_grade, num_classes=n_classes_grade
    ).astype(np.float32),
    "cert_output": y_train_cert.to_numpy(dtype=np.float32),
}
y_test = {
    "grade_output": keras.utils.to_categorical(
        y_test_grade, num_classes=n_classes_grade
    ).astype(np.float32),
    "cert_output": y_test_cert.to_numpy(dtype=np.float32),
}


def build_multitask_model(input_dim):
    inputs = keras.layers.Input(shape=(input_dim,), name="input")
    shared = keras.layers.Dense(64, activation="relu")(inputs)
    shared = keras.layers.Dropout(0.2)(shared)
    grade_output = keras.layers.Dense(
        n_classes_grade, activation="softmax", name="grade_output"
    )(shared)
    cert_output = keras.layers.Dense(
        1, activation="sigmoid", name="cert_output"
    )(shared)
    return keras.Model(inputs=inputs, outputs=[grade_output, cert_output])


model = build_multitask_model(X_train_transformed.shape[1])

if weights_path.is_file():
    model.load_weights(weights_path)
    print(f"Loaded local practice weights: {weights_path}")
else:
    grade_counts = np.bincount(
        np.asarray(y_train_grade, dtype=int), minlength=n_classes_grade
    )
    grade_class_weights = np.asarray(
        [
            len(y_train_grade) / (n_classes_grade * count) if count else 0.0
            for count in grade_counts
        ],
        dtype=np.float32,
    )
    cert_counts = np.bincount(
        np.asarray(y_train_cert, dtype=int), minlength=2
    )
    cert_class_weights = np.asarray(
        [
            len(y_train_cert) / (2 * count) if count else 0.0
            for count in cert_counts
        ],
        dtype=np.float32,
    )

    def weighted_grade_loss(y_true, y_pred):
        class_ids = tf.argmax(y_true, axis=-1, output_type=tf.int32)
        weights = tf.gather(grade_class_weights, class_ids)
        per_row_loss = keras.losses.categorical_crossentropy(y_true, y_pred)
        return per_row_loss * weights

    def weighted_cert_loss(y_true, y_pred):
        class_ids = tf.cast(tf.reshape(y_true, [-1]), tf.int32)
        weights = tf.gather(cert_class_weights, class_ids)
        per_row_loss = keras.losses.binary_crossentropy(y_true, y_pred)
        return per_row_loss * weights

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss={
            "grade_output": weighted_grade_loss,
            "cert_output": weighted_cert_loss,
        },
    )
    model.fit(
        X_train_transformed,
        y_train,
        validation_split=0.1,
        epochs=20,
        batch_size=128,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=4,
                restore_best_weights=True,
            )
        ],
        verbose=0,
    )
    model.save_weights(weights_path)
    # Reload the generated file to confirm the saved weights are usable.
    model.load_weights(weights_path)
    print(f"Trained and saved local practice weights: {weights_path}")

predictions = model.predict(
    X_test_transformed, batch_size=1024, verbose=0
)
pred_cert_probs = np.asarray(predictions[1]).reshape(-1)
pred_cert_labels = (pred_cert_probs >= 0.5).astype(int)
true_cert_labels = np.asarray(y_test["cert_output"]).astype(int)
print(
    "Local certification labels (true/predicted):",
    np.bincount(true_cert_labels, minlength=2),
    np.bincount(pred_cert_labels, minlength=2),
)

correct_cert = np.flatnonzero(
    (true_cert_labels == 1) & (pred_cert_labels == 1)
)
correct_nocert = np.flatnonzero(
    (true_cert_labels == 0) & (pred_cert_labels == 0)
)
if not len(correct_cert) or not len(correct_nocert):
    raise RuntimeError(
        "The local model did not correctly predict both classes. "
        "Delete local_test_model.weights.h5 and rerun to retrain."
    )

student_cert_idx = int(correct_cert[0])
student_nocert_idx = int(correct_nocert[0])
print(
    f"Correct local examples: certified={student_cert_idx}, "
    f"not_certified={student_nocert_idx}"
)

# LIME needs numeric representations for categorical columns.
categorical_names = {}
X_train_lime = X_train.copy()
X_test_lime = X_test.copy()
numerical_medians = {}

for col in numerical_features:
    train_col = pd.to_numeric(X_train_lime[col], errors="coerce")
    test_col = pd.to_numeric(X_test_lime[col], errors="coerce")
    train_col = train_col.replace([np.inf, -np.inf], np.nan)
    test_col = test_col.replace([np.inf, -np.inf], np.nan)
    median = train_col.median()
    if pd.isna(median):
        median = 0.0
    numerical_medians[col] = median
    X_train_lime[col] = train_col.fillna(median)
    X_test_lime[col] = test_col.fillna(median)

for col in categorical_features:
    train_values = X_train_lime[col].fillna("__MISSING__").astype(str)
    test_values = X_test_lime[col].fillna("__MISSING__").astype(str)
    train_cat = pd.Categorical(train_values)
    known_categories = list(train_cat.categories)
    unknown_code = len(known_categories)
    train_codes = train_cat.codes.copy()
    test_codes = pd.Categorical(
        test_values, categories=known_categories
    ).codes.copy()
    test_codes[test_codes < 0] = unknown_code
    feature_idx = X_train.columns.get_loc(col)
    categorical_names[feature_idx] = known_categories + ["__UNKNOWN__"]
    X_train_lime[col] = train_codes
    X_test_lime[col] = test_codes

categorical_features_idx = [
    X_train.columns.get_loc(col) for col in categorical_features
]
X_train_lime_array = X_train_lime.to_numpy(dtype=float)
X_test_lime_array = X_test_lime.to_numpy(dtype=float)


def predict_fn_cert(data_numpy):
    data = np.asarray(data_numpy, dtype=float)
    if data.ndim == 1:
        data = data.reshape(1, -1)

    frame = pd.DataFrame(data, columns=X_train.columns)

    for idx in categorical_features_idx:
        col = X_train.columns[idx]
        categories = np.asarray(categorical_names[idx], dtype=object)
        codes = np.nan_to_num(
            data[:, idx],
            nan=len(categories) - 1,
            posinf=len(categories) - 1,
            neginf=len(categories) - 1,
        ).astype(int)
        valid = (codes >= 0) & (codes < len(categories))
        decoded = np.full(len(codes), "__UNKNOWN__", dtype=object)
        decoded[valid] = categories[codes[valid]]
        frame[col] = decoded

    for col in numerical_features:
        values = pd.to_numeric(frame[col], errors="coerce")
        values = values.replace([np.inf, -np.inf], np.nan)
        frame[col] = values.fillna(numerical_medians[col])

    transformed = preprocessor.transform(frame)
    if sp.issparse(transformed):
        transformed = transformed.toarray()
    outputs = model(
        np.asarray(transformed, dtype=np.float32), training=False
    )
    cert_probs = np.asarray(outputs[1]).reshape(-1, 1)
    return np.hstack((1.0 - cert_probs, cert_probs))


explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train_lime_array,
    feature_names=X_train.columns.tolist(),
    class_names=["not_certify", "certify"],
    categorical_features=categorical_features_idx,
    categorical_names=categorical_names,
    mode="classification",
    discretize_continuous=False,
    feature_selection="highest_weights",
    random_state=42,
)

explanation_cert = explainer.explain_instance(
    data_row=X_test_lime_array[student_cert_idx],
    predict_fn=predict_fn_cert,
    num_features=min(10, X_train_lime_array.shape[1]),
    num_samples=200,
)
explanation_nocert = explainer.explain_instance(
    data_row=X_test_lime_array[student_nocert_idx],
    predict_fn=predict_fn_cert,
    num_features=min(10, X_train_lime_array.shape[1]),
    num_samples=200,
)

print("\nCertified student explanation:")
print(explanation_cert.as_list())
print("\nNot-certified student explanation:")
print(explanation_nocert.as_list())
