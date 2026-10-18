import numpy as np
import tensorflow as tf
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical 

# ==========================================
# 1. Carga y preparación de los datos
# ==========================================
iris_data = load_iris()
X = iris_data.data
y = iris_data.target

# Transformar las etiquetas (0, 1, 2) a matrices binarias One-Hot
Y = to_categorical(y, num_classes=3)

# Separar los datos en conjuntos de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# ==========================================
# 2. Definición de la arquitectura del modelo
# ==========================================
model = tf.keras.Sequential([
    # Capa oculta con 8 neuronas y activación ReLU
    tf.keras.layers.Dense(8, activation='relu', input_shape=(4,)),
    # Capa de salida con 3 neuronas (una por clase) y activación Softmax
    tf.keras.layers.Dense(3, activation='softmax')
])

# ==========================================
# 3. Compilación del modelo
# ==========================================
# Configuramos el optimizador Adam y la función de pérdida para clasificación
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# 4. Entrenamiento desde cero
# ==========================================
print("Iniciando el entrenamiento...")
model.fit(
    X_train, 
    y_train, 
    epochs=60,       # Número de pasadas completas por los datos
    batch_size=8,    # Tamaño del lote de datos por actualización
    verbose=1        # Muestra el progreso en la terminal
)

# ==========================================
# 5. Evaluación final con datos no vistos
# ==========================================
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'\nPrecisión final en el conjunto de prueba: {accuracy:.2%}')