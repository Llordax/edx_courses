def main():
    # prompt the user to input a time in a format of 24-hour
    input_time = input("What time is it? ")

    # convert the time string into a float representing hours
    hours = convert(input_time)

    # check if the time falls within the breakfast range
    if 7.0 <= hours <= 8.0:
        print("breakfast time")

    # check if the time falls within the breakfast range
    elif 12.0 <= hours <= 13.0:
        print("lunch time")

    # check if the time falls within the breakfast range
    elif 18.0 <= hours <= 19.0:
        print("dinner time")

def convert(time):
    # split the time string int hours and minutes using the colon as a separator
    hours_str, minutes_str = time.split(":")

    # convert both string values into float values
    hours = float(hours_str)
    minutes = float(minutes_str)

    # convert minutes into a fraction of an hour and add it to the total of hours
    return hours + (minutes / 60.0)

if __name__ == "__main__":
    main()

