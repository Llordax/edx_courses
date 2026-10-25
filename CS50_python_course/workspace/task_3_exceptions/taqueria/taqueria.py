def main():
    # Define a dictionary containing menu items as keys and their corresponding prices as values
    menu = {
        "Baja Taco": 4.25,
        "Burrito": 7.50,
        "Bowl": 8.50,
        "Nachos": 11.00,
        "Quesadilla": 8.50,
        "Super Burrito": 8.50,
        "Super Quesadilla": 9.50,
        "Taco": 3.00,
        "Tortilla Salad": 8.00,
    }

    # Initialize a variable to track the cumulative total cost of the order
    total_cost = 0.0

    # Start an infinite loop to continually accept item orders from the user
    while True:
        try:
            # Prompt the user to input a menu item
            item = input("Item: ")

            # Capitalize the input string to match the title-case style of the menu dictionary keys
            item_formatted = item.title()

            # Check if the formatted item exists within the menu dictionary
            if item_formatted in menu:
                # Add the item price to the running total
                total_cost += menu[item_formatted]
                 # Print the updated total cost formatted to two decimal places
                print(f"Total: ${total_cost:.2f}")

        # Catch the EOFError (Ctrl+D or Ctrl+Z) to gracefully terminate input collection
        except EOFError:
            print()
            return True

        # Catch any KeyError (though handled safely by the 'in' check above) to keep the loop running
        except KeyError:
            continue

main()
