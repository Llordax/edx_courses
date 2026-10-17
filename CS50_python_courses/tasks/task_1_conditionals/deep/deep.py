def main():
    # Prompt the user for the answer to the Great Question
    answer = input("What is the Answer to the Great Question of Life, the Universe and Everything? ")

    # Clean the input: convert to lowercase and remove any leading/trailing spaces
    cleaned_answer = answer.strip().lower()

    # Check if the answer matches 42, forty-two, or forty two
    if cleaned_answer == "42" or cleaned_answer == "forty-two" or cleaned_answer == "forty two":
        print("Yes")
    else:
        print("No")

main()
