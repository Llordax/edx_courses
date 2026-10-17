# Defining a function to replace ':)' and ':(' for emoticons
def convert(text):
    return text.replace(":)", "🙂").replace(":(", "🙁")

# Defining main function
def main():

    # request input from the user
    text = input("Send me a emoji ':)' or ':(' ")

    # convert function calling
    text = convert(text)

    # print input
    print(text)

# main function calling
main()


