import re

def main():
    # Prompt the user for a text string and print the integer returned by the count function
    print(count(input("Text: ")))

def count(s):
    # Define a regular expression pattern to match the exact word "um"
    # The \b markers represent word boundaries, ensuring it only matches whole words
    pattern = r"\bum\b"
    
    # Search the input string 's' and find all non-overlapping occurrences of the pattern
    # re.IGNORECASE makes the search case-insensitive (matches "um", "Um", "UM")
    matches = re.findall(pattern, s, re.IGNORECASE)

    # Return the total count of matches by checking the length of the resulting list
    return len(matches)

if __name__ == "__main__":
    main()
