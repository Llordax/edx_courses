def main():
    # Prompt the user for a greeting
    greeting = input("Greeting: ")

    # Clean the input: remove leading spaces and convert to lowercase
    cleaned_greeting = greeting.strip().lower()

    # Check if the greeting starts with "hello"
    if cleaned_greeting.startswith("hello"):
        print("$0")
    # Check if the greeting starts with the letter "h" (but is not "hello")
    elif cleaned_greeting.startswith("h"):
        print("$20")
    # For any other greeting
    else:
        print("$100")

main()
