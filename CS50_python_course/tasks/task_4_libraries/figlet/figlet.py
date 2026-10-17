import random
import sys
from pyfiglet import Figlet

def main():
    # Initialize the Figlet object to access ASCII art text rendering options
    figlet = Figlet()

    # Case 1: No arguments provided (only the script name itself exists in sys.argv)
    if len(sys.argv) == 1:
        # Pick a font entirely at random from the list of all available system fonts
        font = random.choice(figlet.getFonts())
    # Case 2: Three arguments provided, and the first flag is either "-f" or "--font"
    elif len(sys.argv) == 3 and sys.argv[1] in ("-f", "--font"):
         # Extract the font name specified by the user in the third position
        font = sys.argv[2]
        # If the requested font name does not exist in pyfiglet's available fonts
        if font not in figlet.getFonts():
            # Terminate the script immediately with an error message
            sys.exit("Invalid usage")
    # Case 3: Any other number or combination of arguments is considered incorrect formatting
    else:
        # Terminate the script immediately with an error message
        sys.exit("Invalid usage")

    # Prompt the user to enter the text message they want to convert into ASCII art
    text = input("Input: ")
    
    # Configure the Figlet object to use the validated font
    figlet.setFont(font=font)
    
    # Render the input text string into the chosen style and print it to the terminal
    print(figlet.renderText(text))

main()
