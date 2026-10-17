def main():
    # Start an infinite loop to keep asking for a fraction until a valid one is given
    while True:
        fraction = input("Fraction: ")

        try:
            # If there is no forward slash in the input, skip the rest and restart the loop
            if "/" not in fraction:
                continue
            # Split the input string into two parts using the "/" as the delimiter
            x_str, y_str = fraction.split("/")

            # Convert both string parts into integers
            x = int(x_str)
            y = int(y_str)

            # Validate that the numerator is not greater than the denominator and not negative
            if x > y or x < 0:
                continue

            # Calculate the percentage and round it to the nearest whole number
            percentage = round((x / y) * 100)

            # If the percentage is 1% or less, print "E" for Empty
            if percentage <= 1:
                print("E")
            # If the percentage is 99% or more, print "F" for Full    
            elif percentage >= 99:
                print("F")
            # For any other percentage, print the actual number followed by the % sign
            else:
                print(f"{percentage}%")
            # Exit the function entirely, which breaks the infinite loop
            return False
        # Catch instances where input has letters (ValueError) or denominator is 0 (ZeroDivisionError)
        except (ValueError, ZeroDivisionError):
            # Prevent the program from crashing and force the loop to restart
            continue

main()

