def main():
    # Prompt the user to enter a text string via the console
    text = input("Input: ")
    
    # Call the 'shorten' function with the text and print the formatted result
    print(f"Output: {shorten(text)}")


def shorten(word):
    # Initialize an empty list to store characters that are NOT vowels
    word_without_vowels = []
    
    # Loop through each individual character (letter, number, or symbol) in the word
    for char in word:
        # Convert the character to lowercase and check if it is Not in the vowels list
        if char.lower() not in ['a', 'e', 'i', 'o', 'u']:
            # If it is a consonant or symbol, append it to the list
            word_without_vowels.append(char)
    # Join all elements in the list into a single string and return it
    return "".join(word_without_vowels)

# Ensure the main() function runs only if this file is executed directly
if __name__ == "__main__":
    main()
