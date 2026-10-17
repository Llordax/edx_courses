def main():
    # Prompt the user to input a text string via the console
    text = input("Input: ")
    # Call the 'shorten' function with the text and print the resulting string
    print(f"Output: {shorten(text)}")


def shorten(word):
    # Initialize an empty list to store characters that are not vowels
    word_without_vowels = []
    # Iterate through every individual character in the provided word string
    for char in word:
        # Convert the character to lowercase and check if it is NOT a standard vowel
        if char.lower() not in ['a', 'e', 'i', 'o', 'u']:
            # If the character is a consonant, symbol, or space, append it to our list
            word_without_vowels.append(char)
    
    # Combine all the saved list elements into a single continuous string and return it
    return "".join(word_without_vowels)

# Standard Python boilerplate to run main() only when this script is executed directly
if __name__ == "__main__":
    main()
