import sys

def main():
    # Initialize an empty list to store the names entered by the user
    names = []

    # Start an infinite loop to continually collect names
    while True:
        # Read input, remove leading/trailing spaces, and save it to the variable
        try:
            name = input("Name: ").strip()
            # If the user didn't just press enter (the input is not empty), add it to the list
            if name:
                names.append(name)
        # Catch the EOFError (Ctrl+D or Ctrl+Z) to safely break out of the input loop
        except EOFError:
            print() # Print a blank line for clean formatting after the prompt ends
            break
    
    # If no names were entered at all, stop execution and exit the function
    if not names:
        return

    # Check the total number of names collected to determine grammatical formatting
    if len(names) == 1:
        # Single name requires no commas or joining words
        formatted_names = names[0]
    elif len(names) == 2:
        # Two names are joined simply with the word "and"
        formatted_names = f"{names[0]} and {names[1]}"
    else:
        # Three or more names are joined by commas, plus an Oxford comma before the final "and"
        # names[:-1] gets all names except the last one to join them with a comma
        formatted_names = ", ".join(names[:-1]) + f", and {names[-1]}"

    # Print the final formatted farewell message to the console
    print(f"Adieu, adieu, to {formatted_names}")

main()
