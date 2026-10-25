from emoji import emojize

def main():
    # Prompt the user to input a text string containing emoji aliases/shortcodes
    text = input("Input: ")
    
    # Call emojize to convert shortcodes (e.g., ":thumbs_up:") into actual emojis
    # The language="alias" argument allows using common alternative names/shortcodes
    print("Output: " + emojize(text, language = "alias"))

main()
