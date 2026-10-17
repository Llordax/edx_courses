import re
import sys

def main():
    # Prompt the user to enter an IPv4 address and print whether the validation returns True or False
    print(validate(input("IPv4 Address: ")))

def validate(ip):
    # Define a regular expression pattern for a single valid byte (0 to 255)
    # - "25[0-5]": matches numbers from 250 to 255
    # - "2[0-4][0-9]": matches numbers from 200 to 249
    # - "1[0-9]{2}": matches numbers from 100 to 199
    # - "[1-9]?[0-9]": matches single or double digit numbers from 0 to 99
    byte_pattern = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    
    # Construct the full IPv4 pattern by combining four byte patterns separated by literal dots
    # The caret (^) anchors the start of the string and the dollar sign ($) anchors the end
    ipv4_pattern = rf"^{byte_pattern}\.{byte_pattern}\.{byte_pattern}\.{byte_pattern}$"

    # Search the input string for a complete match against our compiled IPv4 pattern
    if re.search(ipv4_pattern, ip):
        return True
    return False

if __name__ == "__main__":
    main()
