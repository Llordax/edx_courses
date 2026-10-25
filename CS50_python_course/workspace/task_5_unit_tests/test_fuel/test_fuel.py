import pytest
# Import the custom functions 'convert' and 'gauge' from your existing fuel module
from fuel import convert, gauge

def test_convert_valid():
    # Verify that standard fractions return their correct integer percentage values
    assert convert("3/4") == 75
    assert convert("1/4") == 25
    # Verify that recurring decimal ratios round properly (1/3 is ~33.333%, rounds to 33)
    assert convert("1/3") == 33
    # Verify that edge cases like zero numerator and full capacity handle correctly
    assert convert("0/4") == 0
    assert convert("4/4") == 100

def test_convert_errors():
    # Verify that a denominator of 0 correctly triggers a ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        convert("4/0")

    # Verify that a numerator larger than the denominator triggers a ValueError
    with pytest.raises(ValueError):
        convert("5/4")

    # Verify that passing non-numeric text triggers a ValueError
    with pytest.raises(ValueError):
        convert("three/four")

    # Verify that passing float values instead of whole integers triggers a ValueError
    with pytest.raises(ValueError):
        convert("3.5/4")

    # Verify that passing negative fractions triggers a ValueError
    with pytest.raises(ValueError):
        convert("-1/4")

def test_gauge():
    # Verify that 0% and 1% return "E" for Empty
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    # Verify that 99% and 100% return "F" for Full
    assert gauge(99) == "F"
    assert gauge(100) == "F"
    # Verify that standard middle-ground percentages return the number with a '%' symbol
    assert gauge(50) == "50%"
