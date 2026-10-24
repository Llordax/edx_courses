import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='keras')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import SGD
from tqdm.keras import TqdmCallback


df = pd.read_csv('clipping/lorentz_set.csv').sample(frac=1, random_state=109) # shuffle DataFrame!

# Split train and test
x_train, x_test, y_train, y_test = train_test_split(df.x, df.y, train_size=0.7, random_state=109)


def plot_history(nn, title='', ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(nn.history.history['loss'], label='Training Loss')
    ax.plot(nn.history.history['val_loss'], label='Validation Loss')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss (MSE)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_lorentz(df, test_idx, ax=None):
    if ax is None:
        ax = plt.gca()
    train_mask = np.ones(df.shape[0], dtype=bool)
    train_mask[test_idx] = False
    ax.scatter(df.x[train_mask],df.y[train_mask], c='b', label='train data')
    ax.scatter(df.x[~train_mask],df.y[~train_mask], c='orange', marker='^', label='test data')
    ax.set_xlabel(r'$\omega$')
    ax.set_ylabel(r'$\epsilon$')
    ax.legend()

plt.figure(figsize = (12,5))
plot_lorentz(df, x_test.index)


# Build the model
inputs = Input(shape=(1,))
x = Dense(50, activation='tanh')(inputs)
x = Dense(50, activation='tanh')(x)
outputs = Dense(1, activation='linear')(x)
NN1 = Model(inputs=inputs, outputs=outputs, name='NN1')
NN1.save_weights('NN1_init.weights.h5')
NN1.summary()


fig, axs = plt.subplots(2,2, figsize=(10,8), sharex=True)
axs = axs.flatten()
lrs = [1e-4, 1e-3, 1e-2, 0.1]
for ax, lr in zip(axs, lrs):
    NN1.load_weights('NN1_init.weights.h5')
    NN1.compile(optimizer=SGD(learning_rate=lr, momentum=0.9, nesterov=False),
                loss='mse')

    NN1.fit(x_train, y_train, 
            validation_data=(x_test, y_test),
            batch_size=32,
            epochs=200,
            verbose=0,
            callbacks=[TqdmCallback()])
    
    plot_history(NN1, title=f'Learning Rate = {lr} + Momentum', ax=ax)
plt.tight_layout()


# Inspect strange behavior in 4th plot above - weights are NaN from lr=0.1 training
# Ouch! Numerical overflow did in our network
NN1.get_weights()


### edTest(test_optimizer_config) ###
NN1.load_weights('NN1_init.weights.h5')

# Compile the neural network with an SGD optimizer with learning rate 0.1,
# momentum 0.9,  and norm clipping 0.1.
sgd_clipnorm = SGD(learning_rate=0.1, momentum=0.9, clipnorm=0.1)


### edTest(test_model_compilation) ###
NN1.compile(optimizer=sgd_clipnorm, loss='mse')

NN1.fit(x_train, y_train, 
        validation_data=(x_test, y_test),
        batch_size=32,
        epochs=200,
        verbose=0,
        callbacks=[TqdmCallback()])

plot_history(NN1, title=f'LR=0.1; momentum=0.9; clipnorm=0.1')


