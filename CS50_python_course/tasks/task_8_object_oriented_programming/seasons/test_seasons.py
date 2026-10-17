from datetime import date
import pytest
# Import the validation logic functions from your existing age calculation module (seasons.py)
from seasons import calculate_minutes, minutes_to_words

def test_calculate_minutes():
    # Verify that a basic one-day difference evaluates exactly to 1,440 minutes (24 hours * 60 minutes)
    assert calculate_minutes("2000-01-01", date(2000, 1, 2)) == 1440
    # Verify that a two-year period (including a leap year) calculates the day count accurately
    # 2000 was a leap year (366 days) + 2001 (365 days) = 731 total days
    assert calculate_minutes("2000-01-01", date(2002, 1, 1)) == 731 * 24 * 60

def test_invalid_date():
    # Verify that passing out-of-range calendar components (like month 13) triggers a SystemExit
    with pytest.raises(SystemExit):
        calculate_minutes("2000-13-45", date.today())
    # Verify that passing textual date descriptions instead of ISO format triggers a SystemExit
    with pytest.raises(SystemExit):
        calculate_minutes("January 1, 2000", date.today())

def test_minutes_to_words():
    # Verify that 525,600 minutes converts to capitalized words with the "and" formatting removed
    assert minutes_to_words(525600) == "Five hundred twenty-five thousand, six hundred minutes"
    # Verify that a one-million threshold metrics breakdown formats commas correctly
    assert minutes_to_words(1051200) == "One million, fifty-one thousand, two hundred minutes"
    # Verify complex multi-million numbers map out hyphenated compounds ("forty-four") correctly
    assert minutes_to_words(2629440) == "Two million, six hundred twenty-nine thousand, four hundred forty minutes"
    # Verify large minutes metrics preserve proper text alignment layout
    assert minutes_to_words(6092640) == "Six million, ninety-two thousand, six hundred forty minutes"
    # Verify that mid-range thousands scale formatting properties pass inspection
    assert minutes_to_words(806400) == "Eight hundred six thousand, four hundred minutes"
