# Import the necessary libraries
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
from tqdm.keras import TqdmCallback


# Run this cell for more readable visuals 
large = 22; med = 16; small = 10
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'axes.linewidth': 2,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.style.use('seaborn-v0_8-white')
plt.rcParams.update(params)


#Load Iris Dataset 
iris = load_iris()

# Get the predictor and response variables
X = iris.data
y = iris.target

# Get the Iris label names
target_names = iris.target_names
print(X.shape, y.shape) 

# Standardize the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)


# Helper function to plot the data as clusters 
# based on the iris species label

def plot3clusters(X, title, vtitle):
    plt.figure()
    
    # Select the colours of the clusters
    colors = ['#A43F98', '#5358E0', '#DE0202']
    lw = 2
    plt.figure(figsize=(9,7));
    for color, i, target_name in zip(colors, [0, 1, 2], target_names):
        plt.scatter(X[y == i, 0], X[y == i, 1], color=color, alpha=1., lw=lw, label=target_name);
   
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title(title)
    plt.xlabel(vtitle + "1")
    plt.ylabel(vtitle + "2")
    plt.show()


### edTest(test_check_ae) ###

# Create an AE and fit it with our data using 2 neurons in the dense layer 
# using keras' functional API

# Get the number of data samples i.e. the number of columns
input_dim = X.shape[1]
output_dim = X.shape[1]

# Specify the number of neurons as 2 for the dense layers
encoding_dim = 2 

# Initialize the Sequential model
autoencoder = tf.keras.Sequential()

# Add the input layer
autoencoder.add(tf.keras.layers.InputLayer(input_shape=(input_dim,)))

# Add a denser layer as the encode layer following the input layer 
# with neurons = encoding_dim and no activation function
autoencoder.add(tf.keras.layers.Dense(encoding_dim))

# Add a denser layer as the decode layer following the encode layer 
# with output_dim as a parameter and no activation function
autoencoder.add(tf.keras.layers.Dense(output_dim))

# Complile the autoencoder model
autoencoder.compile(optimizer='adam', loss='mse')

# View the summary of the autoencoder
autoencoder.summary()


# Use the helper function to plot the model history

# Train the autoencoder for 1000 epochs with a batch size of 16 and shuffle enabled
history = autoencoder.fit(X_scaled, X_scaled,
                epochs=1000,
                batch_size=16,
                shuffle=True,
                validation_split=0.1,
                verbose = 0, 
                callbacks=[TqdmCallback()])

# Plot the loss 
plt.plot(history.history['loss'], color='#FF7E79',linewidth=3, alpha=0.5)
plt.plot(history.history['val_loss'], color='#007D66', linewidth=3, alpha=0.4)
plt.title('Model train vs Validation loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='best')
plt.show()


# Create a model which has input as input_features and 
# output as encoded
encoder = tf.keras.Sequential([autoencoder.layers[0]])

# Predict on the entire data using the encoder model, 
# remember to use X_scaled 
encoded_data = encoder.predict(X_scaled)

# Call the function plot3clusters to plot the predicted data 
# using the encoded layer
plot3clusters(encoded_data, 'Encoded data latent-space', 'dimension ')


### edTest(test_check_dist) ###
# Fill 'Yes' or 'No'
answer = 'Yes'