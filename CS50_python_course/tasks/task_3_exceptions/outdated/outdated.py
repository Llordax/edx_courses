# A list containing the names of all twelve months in order
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

def parse_date(date):
    try:
        # Check if the date uses the numeric format (e.g., "9/8/1636")
        if "/" in date:
            # Split the string by forward slashes into month, day, and year components
            month, day, year = date.split("/")
            # Convert all extracted string values into integers
            month, day, year = int(month), int(day), int(year)
        else:
            # Handle the text format (e.g., "September 8, 1636")
            # Split the string at the first space to isolate the month name
            month_name, rest = date.split(" ", 1)
            # Split the remaining text by the comma and space to isolate day and year
            day_text, year = rest.split(", ")
            # Find the month's 1-based index and convert day and year into integers
            month, day, year = MONTHS.index(month_name) + 1, int(day_text), int(year)

    # Catch errors if splitting fails, conversion to int fails, or month name is not found
    except(ValueError, IndexError):
        return None

    # Perform basic validation to ensure month and day numbers fall into acceptable ranges
    if not 1 <= month <= 12 or not 1 <= day <= 31:
        return None

    # Return the validated components as a tuple
    return year, month, day

def main():
    # Start an infinite loop to continually ask the user for input until it passes validation
    while True:
        # Call parse_date with the user's input string
        parsed = parse_date(input("Date: "))
        # If the input was valid and did not return None
        if parsed:
            year, month, day = parsed
            # Print the date padded with leading zeros (4 digits for year, 2 for month and day)
            print(f"{year:04}-{month:02}-{day:02}")
            # Exit the loop and terminate the function execution
            return

main()

