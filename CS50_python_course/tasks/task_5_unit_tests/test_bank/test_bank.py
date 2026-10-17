# Import the 'value' function from your existing bank script/module
from bank import value

def test_hello():
    # Verify that standard lowercase "hello" returns 0 dollars
    assert value("hello") == 0
    # Verify that titlecase "Hello" handles case insensitivity and returns 0 dollars
    assert value("Hello") == 0
    # Verify that a longer phrase starting with uppercase "HELLO" returns 0 dollars
    assert value("HELLO, friend") == 0

def test_starts_with_h():
    # Verify that a non-hello phrase starting with lowercase 'h' returns 20 dollars
    assert value("hi") == 20
    # Verify that a non-hello phrase starting with uppercase 'H' returns 20 dollars
    assert value("Hey") == 20
    # Verify that a longer greeting starting with 'H' returns 20 dollars
    assert value("Howdy") == 20

def test_other_greetings():
    # Verify that questions or phrases not starting with 'h' return 100 dollars
    assert value("What's up?") == 100
    # Verify that formal greetings not starting with 'h' return 100 dollars
    assert value("Good morning") == 100
    # Verify that numeric or non-alphabetic inputs return 100 dollars
    assert value("123 greeting") == 100
