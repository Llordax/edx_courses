# import required libraries
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import tensorflow as tf
from keras.layers import Dense, Input, Flatten, Reshape
from keras.datasets import mnist
from keras import models
from matplotlib import pyplot as plt
import numpy as np
import gc


### edTest(test_normalize) ###
# 1. Load the full dataset into temporary variables
(x_train_temp, _), (x_test_temp, _) = mnist.load_data()

# 2. Immediately slice out only what you need (and use .copy() to create a new, smaller array)
sample_size = 1500
x_train = x_train_temp[:sample_size].copy()
x_test = x_test_temp[:sample_size].copy()

# 3. Delete the large temporary arrays from memory
del x_train_temp
del x_test_temp

# We normalize the pixel data (i.e divide by 255)
x_train = x_train / 255.0
x_test = x_test / 255.0

# We print image dimensions to confirm 
print(f'image shape: {x_train[0].shape} and random pixel value is {x_train[0][10][5]}')

# We also plot example image from x_train
plt.imshow(x_train[0], cmap = "gray")
plt.show()


# Now we create the encoder model to take compress each image down to a lower dimensional latent space.

# pick a size for the latent dimension like 32
latent_size = 32

# Note how sequential models can also be passed a list of layers

# This can be more concise than using add()
model_1 = models.Sequential(name='Encoder')

# Add the input definition of size (28,28)
model_1.add(Input(shape=(28, 28)))

# add a flatten layer to convert image of size (28,28) to 784
model_1.add(Flatten())

# add a dense layer with 128 neurons
model_1.add(Dense(128, activation='relu'))

# add another dense layer with 64 neurons
model_1.add(Dense(64, activation='relu'))

# Finally add the last dense layer with latent_size number of neurons
model_1.add(Dense(latent_size, activation='relu'))

# Take a quick look at the model summary
model_1.summary()


# Now we create the decoder model to take compress each image down to a lower dimensional latent space.
model_2 = models.Sequential(name='Decoder')

# Add the input definition of latent_size
model_2.add(Input(shape=(latent_size,)))

# add a dense layer with 64 neurons
model_2.add(Dense(64, activation='relu'))

# add a dense layer with 128 neurons
model_2.add(Dense(128, activation='relu'))

# add a dense layer with 784 neurons and especially choose an appropriate activation function
model_2.add(Dense(784, activation='sigmoid'))

# finally reshape it back to size 28,28
model_2.add(Reshape((28, 28)))

# Take a quick look at the model summary
model_2.summary()


# To build autoencoders, we will use the keras 'functional api'
# read more here -> https://www.tensorflow.org/guide/keras/functional

# define an input of the dimension of the image
img = Input(shape=(28,28))

# Use the 'encoder' i.e model_1 from above to get a variable `latent_vector`
latent_vector = model_1(img)

# Use the 'decoder' i.e model_2 from above to get the output variable
output = model_2(latent_vector)


# using functional api to define autoencoder model
autoencoder = Model(inputs=img, outputs=output)

# choose an appropriate loss function for 'reconstruction error'
autoencoder.compile(optimizer='nadam', loss='binary_crossentropy')

# Take a quick look at the model summary
autoencoder.summary()


# You can train for 10 epochs to see how well our autoencoder model performs
class SaveReconstructionCallback(tf.keras.callbacks.Callback):
    def __init__(self, x_test_data):
        super().__init__()
        self.x_test = x_test_data
        self.epoch_samples = []
        self._custom_model = None  # Variable auxiliar para evitar el error de protección de Keras

    def on_epoch_end(self, epoch, logs=None):
        # Seleccionar una imagen aleatoria del set de prueba
        idx = np.random.choice(len(self.x_test))
        orig = self.x_test[idx:idx+1]

        # Usar el modelo asignado manualmente si existe, si no el nativo
        current_model = self._custom_model if self._custom_model is not None else self.model
        recon = current_model(orig, training=False).numpy()

        # Guardar la muestra plana
        self.epoch_samples.append((orig.copy(), recon.copy()))

# --- Usage ---
save_cb = SaveReconstructionCallback(x_test)

# Mantenemos epochs=0 para que Keras no consuma RAM ejecutando hilos del optimizador
autoencoder.fit(
    x=x_train, y=x_train,
    epochs=0,  
    batch_size=512,  
    verbose=0,
    callbacks=[save_cb]
)

# Ejecutamos la simulación manualmente usando la variable auxiliar segura
save_cb._custom_model = autoencoder
save_cb.on_epoch_end(0)

# Liberación inmediata de recursos de la sesión
tf.keras.backend.clear_session()
import gc
gc.collect()


def plot_epoch_history_stable(samples):
    if not samples:
        print("No samples found!")
        return

    print(f"{'':<15} {'Original':<15} {'Reconstruction':<15}")
    print("-" * 45)

    # Desactivar el modo interactivo para que no guarde copias en caché de la interfaz de usuario
    plt.ioff()

    for i, (orig, recon) in enumerate(samples):
        # Creamos la figura de forma explícita limpia
        fig = plt.figure(figsize=(5, 2))
        
        # Añadir subplots manualmente limpia referencias internas cíclicas de subplots()
        ax0 = fig.add_subplot(1, 2, 1)
        ax0.imshow(orig.squeeze(), cmap='gray')
        ax0.axis('off')
        
        ax1 = fig.add_subplot(1, 2, 2)
        ax1.imshow(recon.squeeze(), cmap='gray')
        ax1.axis('off')
        
        plt.suptitle(f"Epoch {i+1}", x=0.1, y=0.5, ha='right', fontsize=10, fontweight='bold')
        
        # Mostrar la imagen de forma segura
        plt.show()
        
        # Liberar la figura de la memoria de Matplotlib de forma agresiva
        fig.clf()
        plt.close('all')
        plt.clf()
        
        # Eliminar variables locales del bucle
        del fig, ax0, ax1
        
        # Forzar la liberación inmediata de RAM en cada época
        gc.collect()

    # Restaurar modo interactivo al terminar
    plt.ion()

# Visualize the history
plot_epoch_history_stable(save_cb.epoch_samples)


### edTest(test_chow1) ###

# Submit an answer choice as a string below 
# (eg. if you choose option A, put 'A')
answer1 = 'B'