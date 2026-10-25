# Import the necessary libraries
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm.keras import TqdmCallback
import tensorflow as tf
from keras import layers
from keras import models
from keras import optimizers
from keras import regularizers
import keras.backend as K
np.random.seed(0)
tf.random.set_seed(0)
import gc
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# Use the helper code below to generate the data

# Defines the number of data points to generate
num_points = 50 

# Generate predictor points (x) between 0 and 5
x = np.linspace(0,5,num_points)

# Generate the response variable (y) using the predictor points
y = x * np.sin(x) + np.random.normal(loc=0, scale=1, size=num_points)

# Generate data of the true function y = x*sin(x) 
# x_b will be used for all predictions below 
x_b = np.linspace(0,5,100)
y_b = x_b*np.sin(x_b)


# Split the data into train, valid and test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.3, random_state=42)


# Helper code to plot the generated data 

plt.rcParams["figure.figsize"] = (10,8)

# Plot the train data
plt.plot(x_train,y_train, '.', label='Train data', markersize=15, color='#FF9A98')

# Plot the valid data
plt.plot(x_val,y_val, '.', label='Valid data', markersize=15, color='#F5C500')

# Plot the test data
plt.plot(x_test,y_test, '.', label='Test data', markersize=15, color='#75B594')

# Plot the true data
plt.plot(x_b, y_b, '-', label='True function', linewidth=3, color='#5E5E5E')

# Set the axes labels
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()


# Building an unregularized NN. 
# Initialise the NN, give it an appropriate name for
# the ease of reading
# The FCNN has 5 layers, each with 100 nodes
model_1 = models.Sequential(name='Unregularized')

# Add the input definition
model_1.add(layers.Input(shape=(1,)))

# Add 5 hidden layers with 100 neurons each
model_1.add(layers.Dense(100,  activation='relu'))
model_1.add(layers.Dense(100,  activation='relu'))
model_1.add(layers.Dense(100,  activation='relu'))
model_1.add(layers.Dense(100,  activation='relu'))
model_1.add(layers.Dense(100,  activation='relu'))

# Add the output layer with one neuron 
model_1.add(layers.Dense(1,  activation='linear'))

# View the model summary
model_1.summary()


# Compile the model
model_1.compile(loss='MSE',optimizer=optimizers.Adam(learning_rate=0.001)) 

# Save the history about the model
history_1 = model_1.fit(x_train, y_train, validation_data=(x_val,y_val), epochs=1500, batch_size=10, verbose=0, callbacks=[TqdmCallback()])


### edTest(test_mse) ###

# Use the model above to predict for x_b (used exclusively for plotting)
y_pred = model_1.predict(x_b)

# Use the model above to predict on the test data
y_pred_test = model_1.predict(x_test)

# Compute the MSE on the test data
mse = mean_squared_error(y_test, y_pred_test )


model_2 = models.Sequential(name='Dropout_regularized')

# Add the input definition
model_2.add(layers.Input(shape=(1,)))

# hidden layer with 100 neurons (or nodes)
model_2.add(layers.Dense(100, activation='relu'))
# Add dropout layers with 20% dropout
model_2.add(layers.Dropout(0.2))
model_2.add(layers.Dense(100, activation='relu'))
model_2.add(layers.Dropout(0.2))
model_2.add(layers.Dense(100, activation='relu'))
model_2.add(layers.Dropout(0.2))
model_2.add(layers.Dense(100, activation='relu'))
model_2.add(layers.Dropout(0.2))
model_2.add(layers.Dense(100, activation='relu'))
model_2.add(layers.Dropout(0.2))

# output layer, one neuron 
model_2.add(layers.Dense(1,  activation='linear'))


# Compile the model with MSE as loss and Adam optimizer
# with learning rate as 0.001
model_2.compile(loss='MSE', optimizer=optimizers.Adam(learning_rate=0.001))

# Save the history about the model after fitting on the train data
# Use the validation data and train with 1500 epochs and batch size of 10
# Optionally, use TqdmCallback() with verbose=0 to visualize training progress
history_2 = model_2.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=1500, batch_size=10, verbose=0, callbacks=[TqdmCallback()])


# Helper function to plot the data
# Plot the MSE of the model
plt.rcParams["figure.figsize"] = (10,8)
plt.title("Dropoutegularized")
plt.semilogy(history_2.history['loss'], label='Train Loss', color='#FF9A98', linewidth=2)
plt.semilogy(history_2.history['val_loss'],  label='Validation Loss', color='#75B594', linewidth=2)
plt.legend()

# Set the axes labels
plt.xlabel('Epochs')
plt.ylabel('Log MSE Loss')
plt.legend()
plt.show()


### edTest(test_mse_dropout) ###

# Predict your model on x_b (used exclusively for plotting)
y_pred_dropout = model_2.predict(x_b)

# Predict your model on the test data 
y_pred_test_dropout = model_2.predict(x_test)

# Compute the MSE on the test data
mse_dropout = mean_squared_error(y_test, y_pred_test_dropout)


# Free up RAM to stay within EdStem limits and prevent kernel crashes
del model_1
del history_1
del model_2
del history_2
K.clear_session()
gc.collect()


# Use the helper code to plot the predicted data

# Plotting the predicted data using the L2 regularized model
plt.rcParams["figure.figsize"] = (10,8)

plt.plot(x_b, y_pred_dropout, label='Dropout regularized', color='black', linewidth=2)

# Plotting the predicted data using the unregularized model
plt.plot(x_b, y_pred, label = 'Unregularized model', color='#005493', linewidth=2)

# Plotting the data
plt.plot(x_train,y_train, '.', label='Train data', markersize=15, color='#FF9A98')
plt.plot(x_val,y_val, '.', label='Valid data', markersize=15, color='#F5C500')
plt.plot(x_test,y_test, '.', label='Test data', markersize=15, color='#75B594')

# Set the axes labels
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()


# Print the MSE for all models
from prettytable import PrettyTable

pt = PrettyTable()

pt.field_names = ["Model", "Test MSE"]

pt.add_row(["Unregularized NN", mse ])
pt.add_row(["Dropout NN", mse_dropout ])
print(pt)


### edTest(test_chow1) ###
# Submit an answer choice as a string below 
# (eg. if you choose option A, put 'A')
answer1 = 'B'