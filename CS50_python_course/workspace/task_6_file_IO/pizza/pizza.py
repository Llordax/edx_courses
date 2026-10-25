import csv
import sys
from tabulate import tabulate

def main():
    # Verify that the user provided exactly one command-line argument (the CSV file path)
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    # Extract the file path argument from the second position of the sys.argv list
    file_path = sys.argv[1]

    # Enforce that the target file must have a valid CSV (.csv) extension
    if not file_path.endswith(".csv"):
        sys.exit("Not a CSV file")

    try:
        # Open the specified CSV file in read-only mode using standard UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as file:
            # Create a DictReader object, which maps the information in each row to a dictionary
            # where the keys are the column headers defined in the first row of the CSV
            reader = csv.DictReader(file)

            # Convert the reader stream into a standard Python list of dictionaries
            table_data = list(reader)

            # Format and print the data using tabulate
            # headers="keys" automatically uses the dictionary keys (the CSV column names) as headers
            # tablefmt="grid" applies a clean box-like border around all cells
            print(tabulate(table_data, headers="keys", tablefmt="grid"))

    # Handle the error gracefully if the specified CSV file cannot be found on the system
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()
