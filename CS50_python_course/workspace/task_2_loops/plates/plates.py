def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(str):
    # Requirement 1: Length must be between 2 and 6 characters
    if not (2 <= len(str) <= 6):
        return False

    # Requirement 2: Must start with at least two letters
    if not (str[0].isalpha() and str[1].isalpha()):
        return False

    # Requirement 3 & 4: Numbers must be at the end, and the first number cannot be '0'
    # Requirement 5: No periods, spaces, or punctuation marks allowed

    # Track if we have encountered a number yet
    number_started = False

    for char in str:
        # Check for punctuation, spaces, or periods
        if not char.isalnum():
            return False

        # If the character is a digit
        if char.isdigit():
            # If it's the very first number encountered and it is '0', it's invalid
            if not number_started and char == '0':
                return False
            # Mark that numbers have started
            number_started = True

        # If the character is a letter but numbers have already started, it's invalid
        elif char.isalpha() and number_started:
            return False

    # If all checks passed, the plate is valid
    return True

main()
