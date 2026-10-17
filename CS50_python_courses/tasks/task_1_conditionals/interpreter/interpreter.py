def main():
   # Split the input expression immediately into a list of parts
    parts = input("Expression: ").split()

    # Extract and convert operands directly into integer variables
    x = int(parts[0])
    y = (parts[1])
    z = int(parts[2])

    # Initialize a float variable to store the mathematical result
    result = 0.0

    # Execute the calculation based on the math operator
    if y == "+":
        result = float(x + z)
    elif y == "-":
        result = float(x - z)
    elif y == "*":
        result = float(x * z)
    elif y == "/":
        result = float(x / z)

    # Output the numeric result formatted to one decimal place
    print(f"{result:.1f}")

main()

