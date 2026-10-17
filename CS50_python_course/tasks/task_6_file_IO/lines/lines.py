import sys

def main():
    # Verify that the user provided exactly one command-line argument (the file path)
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    # Extract the file path argument from the second position of the sys.argv list
    file_path = sys.argv[1]

    # Enforce that the target file must have a valid Python (.py) extension
    if not file_path.endswith(".py"):
        sys.exit("Not a Python file")

    try:
        # Open the specified file in read-only mode, safely ignoring decoding errors
        with open(file_path, "r", errors="ignore") as file:
            # Initialize a counter to track valid lines of code
            loc_count = 0

            # Loop through the file line by line
            for line in file:
                # Remove any leading and trailing whitespace (spaces, tabs, newlines)
                stripped_line = line.strip()
                # Skip the line if it is entirely empty or if it starts with a '#' comment symbol
                if stripped_line == "" or stripped_line.startswith("#"):
                    continue

                # If the line contains actual code, increment our counter
                loc_count += 1

            # Print the final total count of lines of code to the console
            print(loc_count)

    # Handle the error gracefully if the specified file cannot be found on the system
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()
