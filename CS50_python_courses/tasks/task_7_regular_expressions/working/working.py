import re

def main():
    # Prompt the user for a time range string and print the converted 24-hour time range
    print(convert(input("Hours: ")))

def convert(s):
    # Define a regex pattern to extract starting and ending times
    # - "^" and "\$": Anchor the pattern to match the complete string
    # - "([0-9]+)": Captures the hour digits
    # - "(?::([0-9]+))?": An optional non-capturing group that contains a capturing group for minutes
    # - "\s(AM|PM)": Matches a space followed by either "AM" or "PM"
    # - "\sto\s": Matches the literal separator string " to "
    pattern = r"^([0-9]+)(?::([0-9]+))?\s(AM|PM)\sto\s([0-9]+)(?::([0-9]+))?\s(AM|PM)$"
    match = re.search(pattern, s)

    # If the input text structural format does not match the regular expression pattern
    if not match:
        raise ValueError("Invalid format")

    # Unpack the regex capture groups into individual string components
    hr1_str, min1_str, meridiem1 = match.group(1), match.group(2), match.group(3)
    hr2_str, min2_str, meridiem2 = match.group(4), match.group(5), match.group(6)

    # Reject leading zeros in hours if the string has multiple digits (e.g., "09 AM" is invalid)
    if (len(hr1_str) > 1 and hr1_str.startswith("0")) or (len(hr2_str) > 1 and hr2_str.startswith("0")):
        raise ValueError("Invalid hour formatting")

    # Convert the hour components from strings to numeric integers
    hr1 = int(hr1_str)
    hr2 = int(hr2_str)

    # Validate that the 12-hour format hour values stay strictly within the 1 to 12 boundary range
    if hr1 < 1 or hr1 > 12 or hr2 < 1 or hr2 > 12:
        raise ValueError("Hour out of range")

    # Process minutes for the starting time
    if min1_str is not None:
        # Enforce that minutes must be exactly 2 digits and cannot exceed 59 minutes
        if len(min1_str) != 2 or int(min1_str) > 59:
            raise ValueError("Invalid minutes")
        min1 = min1_str
    else:
        # If no minutes were supplied in the input (e.g., "9 AM"), default them to "00"
        min1 = "00"

    # Process minutes for the ending time
    if min2_str is not None:
        # Enforce that minutes must be exactly 2 digits and cannot exceed 59 minutes
        if len(min2_str) != 2 or int(min2_str) > 59:
            raise ValueError("Invalid minutes")
        min2 = min2_str
    else:
        # If no minutes were supplied in the input (e.g., "5 PM"), default them to "00"
        min2 = "00"

    # Convert the starting hour into 24-hour format logic
    if meridiem1 == "PM" and hr1 != 12:
        hr1 += 12 # Add 12 hours for afternoon/evening times (except 12 PM)
    elif meridiem1 == "AM" and hr1 == 12:
        hr1 = 0   # Convert 12 AM midnight to hour 0

    # Convert the ending hour into 24-hour format logic
    if meridiem2 == "PM" and hr2 != 12:
        hr2 += 12 # Add 12 hours for afternoon/evening times (except 12 PM)
    elif meridiem2 == "AM" and hr2 == 12:
        hr2 = 0   # Convert 12 AM midnight to hour 0

    # Format hours with a leading zero if they are a single digit (`:02`) and return the text
    return f"{hr1:02}:{min1} to {hr2:02}:{min2}"

if __name__ == "__main__":
    main()
