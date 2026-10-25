import re
import sys
from datetime import date
import inflect

def main():
    # Prompt the user to enter their date of birth via the console
    dob_input = input("Date of Birth: ")
    # Compute the total elapsed minutes between the birth date and today's date
    minutes = calculate_minutes(dob_input, date.today())
    # Convert the resulting integer minutes into an English words string
    output_text = minutes_to_words(minutes)
    # Output the final capitalized textual sentence to the console
    print(output_text)

def calculate_minutes(dob_str, today_date):
    try:
        # Attempt to parse the user's input string into a standard datetime.date object
        dob = date.fromisoformat(dob_str)
    # Handle structural or range errors if the input string doesn't follow the YYYY-MM-DD format
    except ValueError:
        sys.exit("Invalid date")

    # Subtract the birth date from today's date to obtain a timedelta duration object
    diff = today_date - dob
    # Multiply total elapsed days by 24 hours and 60 minutes to compute total minutes
    return diff.days * 24 * 60

def minutes_to_words(minutes):
    # Initialize the inflect library engine to gain access to number-to-text conversion tools
    p = inflect.engine()
    # Convert the integer minutes into text (e.g., 500 becomes "five hundred")
    words = p.number_to_words(minutes, wantlist=False)

    # Use regular expressions to find and remove the word "and" when it acts as a standalone word
    words = re.sub(r'\band\b', '', words)
    # Replace any accidental duplicate spaces with a single space character and trim the boundaries
    words = re.sub(r'\s+', ' ', words).strip()
    # Correct any formatting artifacts where a space mistakenly precedes a comma
    words = words.replace(" ,", ",")

    # Return the clean text string with the first letter capitalized and append the word "minutes"
    return f"{words.capitalize()} minutes"

if __name__ == "__main__":
    main()
