# Import the 'is_valid' function from your existing license plate validation module
from plates import is_valid

def test_length():
    # Verify that the minimum valid length (2 characters) passes
    assert is_valid("AA") is True
    # Verify that the maximum valid length (6 characters) passes
    assert is_valid("ABCDEF") is True
    # Verify that a string under 2 characters fails
    assert is_valid("A") is False
    # Verify that a string over 6 characters fails
    assert is_valid("AAAAAAA") is False

def test_start_letters():
    # Verify that starting with two letters followed by numbers passes
    assert is_valid("AA12") is True
    # Verify that starting with only one letter fails
    assert is_valid("A123") is False
    # Verify that starting with numbers instead of letters fails
    assert is_valid("12AA") is False

def test_numbers_placement():
    # Verify that numbers positioned correctly at the very end pass
    assert is_valid("AAA22") is True
    # Verify that a plate fails if its very first number is a '0'
    assert is_valid("AAA02") is False
    # Verify that a plate fails if a letter appears after a number sequence has started
    assert is_valid("AAA22A") is False

def test_punctuation():
    # Verify that a plate containing a period punctuation mark fails
    assert is_valid("PI3.14") is False
    # Verify that a plate containing an empty whitespace character fails
    assert is_valid("AA 12") is False
    # Verify that a plate containing an exclamation point symbol fails
    assert is_valid("AA!12") is False
