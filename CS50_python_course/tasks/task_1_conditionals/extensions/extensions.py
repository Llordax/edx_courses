def main():
    # promt the user for the name of a file
    file_name = input("File name: ")

    # clean the input: convert to lowercase and remove any leading spaces
    cleaned_name = file_name.strip().lower()

    # check the file extension and output the correct extension
    if cleaned_name.endswith(".gif"):
        print("image/gif")
    elif cleaned_name.endswith(".jpg") or cleaned_name.endswith(".jpeg"):
        print("image/jpeg")
    elif cleaned_name.endswith(".png"):
        print("image/png")
    elif cleaned_name.endswith(".pdf"):
        print("application/pdf")
    elif cleaned_name.endswith(".txt"):
        print("text/plain")
    elif cleaned_name.endswith(".zip"):
        print("application/zip")
    else:
        # print a unknown extension
        print("application/octet-stream")

main()
