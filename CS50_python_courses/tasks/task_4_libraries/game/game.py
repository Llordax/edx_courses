import random

def get_positive_int(prompt):
    # Start an infinite loop to ensure we keep asking until a valid number is provided
    while True:
        try:
            # Read input and convert it into an integer
            value = int(input(prompt))
            # Check if the integer is positive (greater than 0)
            if value > 0:
                # Return the valid positive integer, which breaks the loop and exits the function
                return value
        # Catch errors if the user enters letters or symbols instead of a number
        except ValueError:
            # Silently pass and let the loop prompt the user again
            pass

def main():
    # Prompt the user to enter a positive integer to set the upper limit of the game
    level = get_positive_int("Level: ")
    # Select a random integer between 1 and the specified level (inclusive) as the secret target
    target = random.randint(1, level)

    # Start an infinite loop for the guessing phase of the game
    while True:
        # Prompt the user to enter their guess (must be a positive integer)
        guess = get_positive_int("Guess: ")
        # If the user's guess is lower than the secret random target
        if guess < target:
            print("Too small!")
        # If the user's guess is higher than the secret random target
        elif guess > target:
            print("Too large!")
        # If the user's guess matches the target perfectly
        else:
            print("Just right!")
            # Exit the function entirely, ending the game loop
            return False

main()

