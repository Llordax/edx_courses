import random

def main():
    # Prompt the user to select a valid difficulty level (1, 2, or 3)
    level = get_level()
    # Prompt the user to select a valid difficulty level (1, 2, or 3)
    score = 0

    # Loop exactly 10 times to ask 10 math questions
    for _ in range(10):
        # Generate two random numbers based on the chosen difficulty level
        x = generate_integer(level)
        y = generate_integer(level)
        # Calculate the actual correct mathematical answer
        correct_answer = x + y
        # Track the number of attempts made for the current question
        tries = 0

        # Allow the user up to 3 attempts to answer the current question
        while tries < 3:
            try:
                # Prompt the user for their answer and convert it to an integer
                user_answer = int(input(f"{x} + {y} = "))
                # Check if the user's answer is correct
                if user_answer == correct_answer:
                    score += 1 # Increment the player's total score
                    break      # Exit the while loop to proceed to the next math question
                else:
                    print("EEE") # Display an error message for an incorrect answer
                    tries += 1   # Consume one attempt
            # Catch errors if the input is not a number (e.g., text or empty string)
            except ValueError:
                print("EEE") # Display an error message for an invalid input format
                tries += 1   # Consume one attempt

        # If the user failed all 3 attempts, reveal the correct answer
        if tries == 3:
            print(f"{x} + {y} = {correct_answer}")

    # Output the total final score after answering all 10 questions
    print(f"Score: {score}")


def get_level():
    # Start an infinite loop to ensure the user enters a valid option
    while True:
        try:
            # Read input and convert it to an integer
            level = int(input("Level: "))
            # Only accept numbers 1, 2, or 3 as valid difficulty levels
            if level == 1 or level == 2 or level == 3:
                return level # Return the value and break out of the loop
        except ValueError:
             # Silently catch non-integer inputs and re-prompt the user
            pass

def generate_integer(level):
    # Enforce constraints and manually throw an error if an invalid level is passed programmatically
    if level != 1 and level != 2 and level != 3:
        raise ValueError("Level must be 1, 2, or 3")

    # Return a 1-digit number (0 to 9) inclusive
    if level == 1:
        return random.randint(0, 9)
    # Return a 2-digit number (10 to 99) inclusive
    elif level == 2:
        return random.randint(10, 99)
    # Return a 3-digit number (100 to 999) inclusive
    else:
        return random.randint(100, 999)

if __name__ == "__main__":
    main()
