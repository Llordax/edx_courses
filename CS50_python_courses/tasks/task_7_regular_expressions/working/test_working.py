import pytest
# Import the 'convert' function from your existing time converter module (working.py)
from working import convert

def test_valid_conversions():
    # Verify that simple hours without minutes convert accurately to military time
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    # Verify that explicit hours and minutes format strings convert accurately
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
    # Verify that an overnight time range crossing the midday/midnight threshold is handled correctly
    assert convert("8 PM to 8 AM") == "20:00 to 08:00"
    # Verify the tricky 12-hour boundary exceptions (12 AM is 00:00, 12 PM is 12:00)
    assert convert("12 AM to 12 PM") == "00:00 to 12:00"

def test_invalid_times():
    # Verify that minute values exceeding 59 (out of range) successfully raise a ValueError
    with pytest.raises(ValueError):
        convert("8:60 AM to 4:60 PM")
    # Verify that hour values exceeding 12 in the 12-hour system successfully raise a ValueError
    with pytest.raises(ValueError):
        convert("13 AM to 5 PM")
    # Verify that single-digit minutes (invalid format like :7 instead of :07) throw a ValueError
    with pytest.raises(ValueError):
        convert("10:7 AM to 5:1 PM")

def test_invalid_formats():
    # Verify that omitting the required space before the AM/PM meridiem flag triggers a ValueError
    with pytest.raises(ValueError):
        convert("9AM to 5PM")
    # Verify that substituting the literal " to " separator with a dash ("-") triggers a ValueError
    with pytest.raises(ValueError):
        convert("9 AM - 5 PM")
        # Verify that using prohibited leading zeros for the hours segment triggers a ValueError
    with pytest.raises(ValueError):
        convert("09 AM to 5:00 PM")
