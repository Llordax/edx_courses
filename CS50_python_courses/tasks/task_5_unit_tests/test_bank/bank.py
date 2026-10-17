def main():
    # Prompt the user to enter a greeting phrase via the console
    greeting = input("Greeting: ")
    # Pass the user input into the value function to compute the price
    result = value(greeting)
    # Output the calculated monetary value formatted with a dollar sign
    print(f"${result}")

def value(greeting):
    # Clean the input string by removing surrounding whitespace and converting it to lowercase
    cleaned_greeting = greeting.strip().lower()
    
    # Rule 1: If the cleaned phrase starts explicitly with the word "hello"
    if cleaned_greeting.startswith("hello"):
        return 0
    # Rule 2: If it didn't start with "hello" but still begins with the letter "h"
    elif cleaned_greeting.startswith("h"):
        return 20
    # Rule 3: For any other greeting phrase that does not start with "h"
    else:
        return 100

# Standard boilerplate to ensure main() runs only when executing this script directly
if __name__ == "__main__":
    main()
