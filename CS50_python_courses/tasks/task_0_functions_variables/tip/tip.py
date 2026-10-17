# Defining main function
def main():
    # request input from the user with dollars_to_float fucntion calling, all of this stored in a variable
    dollars = dollars_to_float(input("How much was the meal? "))

    # request input from the user with percent_to_float fucntion calling, all of this stored in a variable
    percent = percent_to_float(input("What percentage would you like to tip? "))

    # tip calculation
    tip = dollars * percent

    # print the result formatted to two decimal numbers
    print(f"Leave ${tip:.2f}")

# Function to convert the amount in $ to a float number
def dollars_to_float(d):
    # Remove the leading '$' and convert the remaining string to a float
    return float(d.replace("$", ""))

# Function to convert percentage % to a float number
def percent_to_float(p):
    # Remove the trailing '%' and convert to a float, then divide by 100
    return float(p.replace("%", "")) / 100

# Main function calling
main()
