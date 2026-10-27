import pandas as pd
import numpy as np
import tensorflow as tf
import keras
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

tf.random.set_seed(42)

# Detectar la ruta exacta de la carpeta donde reside este script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'student_data.pqt')

# Load locally generated dataset using the safe absolute path
try:
    final_df = pd.read_parquet(data_path)
    print(f"Data successfully loaded from local Parquet file: {data_path}")
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find 'student_data.pqt' at {data_path}. Please run 'data_generator.py' first.")


### TEST FUNCTION: test_create_targets
n_classes_grade = 4
model_df = final_df.copy()
model_df['certified'] = model_df['certified'].astype(int)

bins = [-0.01, 0.20, 0.70, 0.90, 1.01]
labels = [0, 1, 2, 3]
model_df['performance_bucket'] = pd.cut(model_df['grade'], bins=bins, labels=labels)
model_df['performance_bucket'] = model_df['performance_bucket'].astype(int)


### TEST FUNCTION: test_separate_features_labels
labels_grade = model_df['performance_bucket']
labels_cert = model_df['certified']

columns_to_drop = [col for col in model_df.columns if col not in ['certified', 'performance_bucket', 'grade']]
for col in list(columns_to_drop):
    if any(leak in col.lower() for leak in ['pass', 'status', 'complete', 'fail', 'outcome', 'view', 'explore', 'cert']):
        if col in columns_to_drop:
            pass
    else:
        if col in columns_to_drop:
            columns_to_drop.remove(col)

columns_to_drop = list(set(columns_to_drop + ['certified', 'performance_bucket', 'grade']))
features = model_df.drop(columns=columns_to_drop, errors='ignore')


### TEST FUNCTION: test_identify_feature_types
num_features = features.select_dtypes(include=['number']).columns.tolist()
cat_features = features.select_dtypes(exclude=['number']).columns.tolist()

if 'early_nevents' in cat_features:
    cat_features.remove('early_nevents')
if 'early_nevents' not in num_features and 'early_nevents' in features.columns:
    num_features.append('early_nevents')

categorical_features = cat_features
numerical_features = num_features


### TEST FUNCTION: test_train_test_split
X_train, X_test, y_train_grade, y_test_grade, y_train_cert, y_test_cert = train_test_split(
    features, 
    labels_grade, 
    labels_cert, 
    test_size=0.20, 
    stratify=labels_cert, 
    random_state=42
)


### TEST FUNCTION: test_keras_data_format
from tensorflow.keras.utils import to_categorical
y_train_grade_oh = to_categorical(y_train_grade, num_classes=4).astype(np.float32)
y_test_grade_oh = to_categorical(y_test_grade, num_classes=4).astype(np.float32)

y_train = {
    'grade_output': y_train_grade_oh,
    'cert_output': np.asarray(y_train_cert.values, dtype=np.float32)
}
y_test = {
    'grade_output': y_test_grade_oh,
    'cert_output': np.asarray(y_test_cert.values, dtype=np.float32)
}


### TEST FUNCTION: test_preprocessor
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, numerical_features),
    ('cat', cat_transformer, categorical_features)
])


### TEST FUNCTION: test_transform_data
X_train_transformed = preprocessor.fit_transform(X_train).astype(np.float32)
X_test_transformed = preprocessor.transform(X_test).astype(np.float32)


# --- Custom Weighted Loss Functions ---
def create_weighted_binary_crossentropy(class_weights):
    def weighted_binary_crossentropy(y_true, y_pred):
        weights = tf.gather(class_weights, tf.cast(y_true, tf.int32))
        loss = keras.losses.binary_crossentropy(y_true, y_pred)
        return loss * weights
    return weighted_binary_crossentropy

def create_weighted_categorical_crossentropy(class_weights):
    def weighted_categorical_crossentropy(y_true, y_pred):
        y_true_int = tf.cast(tf.argmax(y_true, axis=-1), tf.int32)
        weights = tf.gather(class_weights, y_true_int)
        loss = keras.losses.categorical_crossentropy(y_true, y_pred)
        return loss * weights
    return weighted_categorical_crossentropy

weights_grade = {i: (1 / count) * len(labels_grade) / n_classes_grade for i, count in enumerate(np.bincount(labels_grade)) if count > 0}
weights_cert = {i: (1 / count) * len(labels_cert) / 2.0 for i, count in enumerate(np.bincount(labels_cert)) if count > 0}
weights_grade_tensor = tf.constant([weights_grade.get(i, 0) for i in range(n_classes_grade)], dtype=tf.float32)
weights_cert_tensor = tf.constant([weights_cert.get(i, 0) for i in range(2)], dtype=tf.float32)
loss_grade_weighted = create_weighted_categorical_crossentropy(weights_grade_tensor)
loss_cert_weighted = create_weighted_binary_crossentropy(weights_cert_tensor)


### TEST FUNCTION: test_model_architecture
def build_multitask_model():
    input_shape = X_train_transformed.shape[1]
    inputs = tf.keras.Input(shape=(input_shape,), name='input_layer')
    
    shared_dense = tf.keras.layers.Dense(64, activation='relu', name='shared_dense')(inputs)
    shared_dropout = tf.keras.layers.Dropout(0.2, name='shared_dropout')(shared_dense)
    
    grade_output = tf.keras.layers.Dense(4, activation='softmax', name='grade_output')(shared_dropout)
    cert_output = tf.keras.layers.Dense(1, activation='sigmoid', name='cert_output')(shared_dropout)
    
    model = tf.keras.Model(inputs=inputs, outputs=[grade_output, cert_output], name='multi_task_model')
    return model

model = build_multitask_model()


### TEST FUNCTION: test_model_compilation
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss={
        'grade_output': loss_grade_weighted,
        'cert_output': loss_cert_weighted
    },
    metrics={
        'grade_output': [keras.metrics.AUC(name='auc_grade')],
        'cert_output': [keras.metrics.AUC(name='auc_cert')]
    }
)


### TEST FUNCTION: test_model_training
print("\nStarting multi-task neural network model training...")
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_cert_output_auc_cert',
    patience=3,
    restore_best_weights=True,
    mode='max'
)

history = model.fit(
    X_train_transformed,
    y_train,
    validation_data=(X_test_transformed, y_test),
    epochs=15,
    batch_size=64,
    callbacks=[early_stopping],
    verbose=1
)


### TEST FUNCTION: test_model_evaluation
print("\nEvaluating model on test dataset...")
results = model.evaluate(X_test_transformed, y_test, verbose=1)
print(f"\nFinal Test Metrics Evaluation:")
print(f"Metrics: {model.metrics_names}")
print(f"Values: {results}")


### TEST FUNCTION: test_save_weights
print("\nSaving local model weights...")
weights_path = os.path.join(script_dir, 'multi_task_model_weights.weights.h5')
model.save_weights(weights_path)
print(f"Weights successfully saved local as '{weights_path}'!")
