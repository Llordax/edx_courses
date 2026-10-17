import csv
import sys

def main():
    # Verify that the user provided exactly two command-line arguments (input file and output file)
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    # Extract the input and output file paths from the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Initialize an empty list to store the dictionaries of cleaned student data
    cleaned_students = []

    try:
        # Open the source CSV file in read-only mode
        with open(input_file, "r") as file:
            # Map the information in each row to a dictionary using the CSV headers
            reader = csv.DictReader(file)
            for row in reader:
                # Split the name string at the comma to separate last and first names
                parts = row["name"].split(",")
                # Ensure the split results in exactly two components (Last and First)
                if len(parts) == 2:
                    last = parts[0].strip() # Remove surrounding whitespace from the last name
                    first = parts[1].strip() # Remove surrounding whitespace from the first name
                else:
                    # Skip rows that do not match the expected "Last, First" format
                    continue

                # Append a new structured dictionary to our cleaned data list
                cleaned_students.append({
                    "first": first,
                    "last": last,
                    "house": row["house"]
                })
    # Handle the error if the specified input file does not exist
    except FileNotFoundError:
        sys.exit(f"Could not read {input_file}")

    try:
        # Open the target file in write mode, ensuring correct newline handling across operating systems
        with open(output_file, "w", newline="") as file:
            # Define the new column header structure for the output CSV file
            fieldnames = ["first", "last", "house"]
            # Initialize a DictWriter object configured with the target fields
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header row ("first,last,house") to the top of the file
            writer.writeheader()
            # Write all the cleaned student dictionary objects as new rows in the file
            writer.writerows(cleaned_students)
    # Catch any unexpected write errors (e.g., permission issues, locked file)
    except Exception:
        sys.exit(f"Could not write {output_file}")

if __name__ == "__main__":
    main()
