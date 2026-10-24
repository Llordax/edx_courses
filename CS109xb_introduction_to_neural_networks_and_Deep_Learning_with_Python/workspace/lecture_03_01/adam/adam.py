# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Import the gradient_descent function from the helper code
# (Nota: Asegúrate de mantener esta línea si tienes el archivo auxiliar en tu workspace)
from gradient_descent import gradient_descent

# Function to compute the response data given the predictor data
def get_response_data(x):
    return np.cos(x) * np.exp(-x/10)

# Generate data for performing the gradient descent with Adam
# Get the 500 predictor data points from -15 to 15
x = np.linspace(-15, 15, 500)

# Generate the response data from predictor data using function
# get_response_data above by passing it the predictor data
y = get_response_data(x)

# Plot the generated data using the helper code given below
plt.plot(x, y, linewidth=3, color='#F5B7B1')
plt.grid(alpha=0.3)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('$X$', fontsize=16)
plt.ylabel('$Y$', fontsize=16)

# Function to compute the derivative
def derivative(W):
    return -0.1 * ((np.exp(-W/10)) * (10*np.sin(W) + np.cos(W)))

# Function to perform gradient descent with Adam optimizer
def adam_descent(W, eta=0.01, rho1=0.9, rho2=0.999, delta=1e-8, tolerance=0.00001):
    
    # Variable to store the W value before update. This will help
    # to check for convergence.
    W_prev = 0
    
    # Initialize v and r to zero
    v = 0
    r = 0
    
    # t is the iteration counter that will be used in the bias
    # correction equations
    t = 0
    
    # Save the current weights to a new list and append the updated
    # weights in each iteration to the same
    Ws = [W]
    
    # Perform the update until convergence
    # Convergence is said to have taken place if
    # the absolute difference between the previous and updated
    # weight is less than the tolerance.
    # Usamos una condición inicial válida para entrar al bucle:
    while t == 0 or np.abs(W - W_prev) >= tolerance:
        
        # Increment the counter t for each iteration
        t += 1
        
        # Compute the gradient of W by calling the derivative function
        g = derivative(W)
        
        # Update the v, the moving average of the gradient according
        # to the equation given in the instructions
        v = rho1 * v + (1 - rho1) * g
        
        # Update the r, the moving average of the squared gradient
        # according to the equation given in the instructions
        r = rho2 * r + (1 - rho2) * (g ** 2)
        
        # According the the bias correct equations get the corrected
        # v and r values
        v_bias_corr = v / (1 - (rho1 ** t))
        r_bias_corr = r / (1 - (rho2 ** t))
        
        # Save the W value in W_prev before update for convergence test
        W_prev = W
        
        # Update the weight parameters based on the equation given
        # in the instructions
        W = W - (eta / (delta + np.sqrt(r_bias_corr))) * v_bias_corr
        
        # Append the new weight list with the adjusted weight value
        Ws.append(W)
        
    return Ws, t


### edTest(test_adam_descent) ###

# Select an eta value that is less than or equal to 1
eta = 0.1

# Plot the descent with Adam starting from 6 random values of W
fig, axes = plt.subplots(3, 2, figsize=(20, 20))

# Run the loop for the number of plots to make
for ax in axes.ravel():
    
    # Initialize the weights to a random value between -15 and
    # 15 (which are the min and max values of x)
    W = np.random.uniform(-15, 15)
    
    # Get the weights after gradient descent with adam and the
    # number of iterations by calling the adam_descent function with the initialized weight and selected epsilon value
    Ws, tg = adam_descent(W, eta=eta)
    
    # Helper function to call gradient_descent function and
    # get number of steps (del código base del curso)
    Wd, ts = gradient_descent(W, eta)
    
    # Print the number of steps taken by gradient descent with
    # and without Adam
    print(f'The number of steps taken by gradient descent is {ts} and the number of steps taken by GD with Adam is {tg}')
    
    # Use the helper function below to plot how descent is working
    # with Adam after initializing in random weight
    
    # Plot the original data
    ax.plot(x, y, color="black", alpha=0.6, linewidth=2)
    ax.scatter(np.array(Ws), get_response_data(np.array(Ws)), s=150, label='transition', color='#F1948A', alpha=0.6)
    
    # Plot the starting point
    ax.scatter(Ws[0], get_response_data(Ws[0]), color='#F39C12', s=150, label='Start', alpha=0.9, edgecolor='black')
    ax.set_title(f'{tg} Steps', fontsize=16)
    
    # Plot the ending point
    ax.scatter(Ws[-1], get_response_data(Ws[-1]), color='#5DADE2', s=150, label='End', edgecolor='black')
    ax.set_xlabel('$X$', fontsize=14)
    ax.set_ylabel('$Y$', fontsize=14)
    ax.legend(loc='best')

plt.tight_layout()
plt.show()