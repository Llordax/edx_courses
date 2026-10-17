def main():
    # Start an infinite loop to repeatedly ask for input until it successfully returns
    while True:
        fraction = input("Fraction: ")
        try:
            # Step 1: Convert the input string fraction into an integer percentage
            percentage = convert(fraction)
            # Step 2: Formulate the graphical output ("E", "F", or the numeric percentage)
            output = gauge(percentage)
            # Print the resulting label to the terminal
            print(output)
            # Exit the entire function, ending the program successfully
            return True

        # Catch data errors or mathematical division issues thrown by the convert function
        except (ValueError, ZeroDivisionError):
            # Bypass the error and jump back to the start of the loop to re-prompt the user
            continue

def convert(fraction):
    # Rule out inputs that do not contain a forward slash separator
    if "/" not in fraction:
        raise ValueError

    # Split the input text into numerator and denominator strings
    x_str, y_str = fraction.split("/")

    # Attempt to cast string portions into standard integer formats
    x = int(x_str)
    y = int(y_str)

    # Prevent divisions where the denominator is explicitly zero
    if y == 0:
        raise ZeroDivisionError

    # Ensure the fraction is logical: numerator cannot exceed denominator or be negative
    if x > y or x < 0:
        raise ValueError

    # Compute the ratio and round it up or down to the nearest whole percentage integer
    return round((x / y) * 100)

def gauge(percentage):
    # If the computed tank capacity is at 1% or less, label it as "E" (Empty)
    if percentage <= 1:
        return "E"
    # If the computed tank capacity is at 99% or higher, label it as "F" (Full)
    elif percentage >= 99:
        return "F"
    # Return the regular calculated value appended with the percentage character sign
    else:
        return f"{percentage}%"

# standard boilerplate check to run main loop code safely upon execution
if __name__ == "__main__":
    main()
