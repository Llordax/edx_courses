from collections import Counter

def main():
    # Initialize a Counter object to automatically track the count of each grocery item
    groceries = Counter()

    try:
        # Start an infinite loop to continuously accept user inputs
        while True:
            # Read input, remove leading/trailing spaces, and convert it to uppercase
            item = input().strip().upper()
            # If the input is not empty, increment its count in the dictionary
            if item:
                groceries[item] += 1
     # Catch the EOFError (Ctrl+D on macOS/Linux or Ctrl+Z on Windows) to stop reading input
    except EOFError:
         # Gracefully pass and exit the loop without crashing the program
        pass

    # Loop through the items sorted alphabetically by their keys  
    for item in sorted(groceries):
        # Print the total count followed by the item name in uppercase
        print(f"{groceries[item]} {item.upper()}")

main()
