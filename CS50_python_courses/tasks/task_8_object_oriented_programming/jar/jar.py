class Jar:
    # The initializer method (constructor) that runs when creating a new Jar object
    def __init__(self, capacity=12):
        # Validate that the capacity provided is a whole number (int) and not negative
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("Capacity must be a non-negative integer")
        # Store the maximum capacity using a protected internal variable format
        self._capacity = capacity
        # Initialize the current number of cookies in the jar to zero
        self._size = 0

    # The string representation method, triggered when calling print() or str() on the object
    def __str__(self):
        # Return a string containing the cookie emoji repeated by the current size count
        return "🍪" * self._size

    # Method to add a specific number of cookies into the jar
    def deposit(self, n):
        # Ensure the amount to deposit is a valid positive integer
        if not isinstance(n, int) or n < 0:
            raise ValueError("Must deposit a positive number of cookies")
        # Prevent the addition if it would make the total cookies exceed the jar's maximum capacity
        if self._size + n > self._capacity:
            raise ValueError("Exceeds jar capacity")
        # Add the cookies to the current size tally
        self._size += n

    # Method to remove a specific number of cookies from the jar
    def withdraw(self, n):
        # Ensure the amount to withdraw is a valid positive integer
        if not isinstance(n, int) or n < 0:
            raise ValueError("Must withdraw a positive number of cookies")
        # Prevent the action if the user attempts to take out more cookies than what is available
        if self._size - n < 0:
            raise ValueError("Not enough cookies in the jar")
        # Subtract the cookies from the current size tally
        self._size -= n

    # A getter property to securely access the private maximum capacity value
    @property
    def capacity(self):
        return self._capacity

    # A getter property to securely access the private current size value
    @property
    def size(self):
        return self._size
