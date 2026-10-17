def main():
    # Prompt the user to enter a license plate string via the console
    plate = input("Plate: ")
    # Pass the input into the is_valid function and print the appropriate verdict
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(str):
    # Rule 1: Check if the plate length is between 2 and 6 characters (inclusive)
    if not (2 <= len(str) <= 6):
        return False

    # Rule 2: The plate must start with at least two letters
    if not (str[0].isalpha() and str[1].isalpha()):
        return False

    # Flag to track whether we have encountered a numeric digit while iterating
    number_started = False

    # Loop through each individual character in the plate string
    for char in str:
        # Rule 3: No periods, spaces, or special characters are allowed (alphanumeric only)
        if not char.isalnum():
            return False

        # Check if the current character is a number
        if char.isdigit():
            # Rule 4: The first number used cannot be a '0'
            if not number_started and char == '0':
                return False
            # Mark that a number sequence has officially started
            number_started = True

        # Rule 5: Letters cannot come after numbers (e.g., AAA22A is invalid)
        elif char.isalpha() and number_started:
            return False

    # If all character checks and constraints pass successfully, return True
    return True

# Standard boilerplate condition to trigger the main execution loop
if __name__ == "__main__":
    main()
