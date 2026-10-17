import validators

def main():
    # Prompt the user to enter their email address and print the returned validity string
    print(validate(input("What's your email address? ")))

def validate(s):
    # Use the validators library to check if the input string follows a proper email syntax
    if validators.email(s):
        # Return "Valid" if the format is correct (e.g., user@example.com)
        return "Valid"
    else:
        # Return "Invalid" if the email format is broken or missing required elements
        return "Invalid"

# Standard Python boilerplate to ensure main() runs only when this file is executed directly
if __name__ == "__main__":
    main()
