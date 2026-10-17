import pytest
# Import the custom 'Jar' class from your existing cookie jar module (jar.py)
from jar import Jar

def test_init():
    # Verify that the default constructor sets the capacity to 12 and the initial size to 0
    jar = Jar()
    assert jar.capacity == 12
    assert jar.size == 0

    # Verify that a custom capacity configuration works as expected
    custom_jar = Jar(5)
    assert custom_jar.capacity == 5

    # Verify that passing a negative capacity value successfully triggers a ValueError
    with pytest.raises(ValueError):
        Jar(-1)
    # Verify that passing an invalid non-integer type successfully triggers a ValueError
    with pytest.raises(ValueError):
        Jar("ten")

def test_str():
    jar = Jar()
    # Verify that an empty jar returns an empty string representation
    assert str(jar) == ""

    # Verify that a jar containing 1 cookie outputs a single cookie emoji
    jar.deposit(1)
    assert str(jar) == "🍪"

    # Verify that adding 3 more cookies scales the string output up to 4 emojis cleanly
    jar.deposit(3)
    assert str(jar) == "🍪🍪🍪🍪"

def test_deposit():
    jar = Jar(10)

    # Verify that a valid deposit increments the internal size accurately
    jar.deposit(5)
    assert jar.size == 5

    # Verify that filling the jar exactly to its maximum capacity threshold succeeds
    jar.deposit(5)
    assert jar.size == 10

    # Verify that attempting to deposit past the capacity boundary raises a ValueError
    with pytest.raises(ValueError):
        jar.deposit(1)

def test_withdraw():
    jar = Jar(10)
    jar.deposit(8)

    # Verify that a valid cookie withdrawal decrements the internal size accurately
    jar.withdraw(3)
    assert jar.size == 5

    # Verify that taking cookies out down to exactly empty (size 0) succeeds
    jar.withdraw(5)
    assert jar.size == 0

    # Verify that attempting to withdraw from an empty jar raises a ValueError
    with pytest.raises(ValueError):
        jar.withdraw(1)
