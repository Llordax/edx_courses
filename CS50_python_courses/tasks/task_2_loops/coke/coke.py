# Initialize the total cost of the Coke
amount_due = 50

# Loop runs as long as there is money left to pay
while amount_due > 0:
    # Print the remaining amount due using exactly the format required
    print(f"Amount Due: {amount_due}")

    # Prompt the user to input a coin
    coin = int(input("Insert Coin: "))

    # Check if the coin is an accepted denomination
    if coin == 25 or coin == 10 or coin == 5:
        # Subtract the coin value from the amount due
        amount_due -= coin

# Calculate the change owed (converts negative values to positive)
change_owed = abs(amount_due)

# Output the final change owed to the user
print(f"Change Owed: {change_owed}")
