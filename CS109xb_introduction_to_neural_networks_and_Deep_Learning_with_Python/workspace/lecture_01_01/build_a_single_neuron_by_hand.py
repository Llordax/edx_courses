# =====================================================================
# SECCIÓN 1: IMPORTAR LIBRERÍAS Y CARGAR DATOS
# =====================================================================

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# Read the dataset
heart_data = pd.read_csv('data/Heart.csv', index_col=0)

# Take a quick look at the dataframe
heart_data.head() 

# =====================================================================
# SECCIÓN 2: DEFINIR VARIABLES Y PRIMER GRÁFICO
# =====================================================================

# Assign Max Heart Rate as the predictor
x = heart_data['MaxHR']

# Assign AHD as the response variable
# Replace the string column values to 0 and 1
y = heart_data['AHD'].replace({'No': 0, 'Yes': 1})

# Plot the predictor and reponse vairables as a scatter plot 
# with appropriate axes label
plt.scatter(x, y, alpha=0.5, label='Data points')
plt.xlabel('MaxHR')
plt.ylabel('Heart Disease (AHD)')
plt.legend(loc='best')  

# =====================================================================
# SECCIÓN 3: COMPONENTES DEL PERCEPTRÓN (FUNCIONES)
# =====================================================================

### edTest(test_affine) ###

# Function to perform affine transformation
def affine(x, w, b):
    """Return affine transformation of x"""
    z = w * x + b
    return z

### edTest(test_sigmoid) ###

# Function to apply sigmoid function on the parameter
def sigmoid(z):
    h = 1 / (1 + np.exp(-z))
    return h  

### edTest(test_neuron_predict) ###

# Function to combine the previous operations
def neuron_predict(x, w, b):
    # Call the previous functions
    z = affine(x, w, b)
    h = sigmoid(z)
    return h

# =====================================================================
# SECCIÓN 4: PARÁMETROS MANUALES Y PREDICCIONES
# =====================================================================

# Manually set the weight and bias parameters.
w = -0.1 
b = 14.5      

# The forward mode or predict of a single neuron

# Create evenly spaced values of x to predict on
x_linspace = np.linspace(x.min(), x.max(), 500) 
h = neuron_predict(x_linspace, w, b)   

# =====================================================================
# SECCIÓN 5: GRÁFICO FINAL CON LA FRONTERA DE DECISIÓN
# =====================================================================

# Plot Predictions
fig, ax = plt.subplots(1, 1, figsize=(11, 7))
ax.scatter(x, y, label=r'Heart Data', alpha=0.2)
ax.plot(x_linspace, h, lw=2, c='orange', label=r'Single Neuron')

# First value in x_linspace with a probability < 0.5
db = x_linspace[np.argmax(h < 0.5)] 
ax.axvline(x=db, alpha=0.3, linestyle='-.', c='r', label='Decision Boundary')

# Proper plot labels are very important!
ax.tick_params(labelsize=16)
plt.xlabel('MaxHR', fontsize=16)
plt.ylabel('Heart Disease (AHD)', fontsize=16)

# Create a legend and make it big enough to read
ax.legend(fontsize=16, loc='best') 
plt.show()   

# =====================================================================
# SECCIÓN 6: EVALUACIÓN DE PÉRDIDA (LOSS) Y PRECISIÓN (ACCURACY)
# =====================================================================

def loss(y_true, y_pred, eps=1e-15):
    assert y_true.shape == y_pred.shape
    # Clipping
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -sum(y_true * np.log(y_pred) + (1 - y_true) * (np.log(1 - y_pred)))   

## Print the loss of the single neuron model
h_pred = neuron_predict(x, w, b)
print("Loss:", loss(y, h_pred))   

def accuracy(y_true, y_pred):
    assert y_true.shape == y_pred.shape
    return sum(y_true == (y_pred >= 0.5).astype(int)) / len(y_true)   

### edTest(test_performance) ###

# For the baseline predictions are all ones
baseline_acc = accuracy(y, np.ones(len(y))) 
perceptron_acc = accuracy(y, h_pred)

print(f'Baseline Accuracy: {baseline_acc:.2%}')
print(f'Perceptron Accuracy: {perceptron_acc:.2%}')