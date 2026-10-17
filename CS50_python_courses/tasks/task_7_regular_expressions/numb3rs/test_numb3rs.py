# Import the 'validate' function from your existing IPv4 validation module (numb3rs.py)
from numb3rs import validate

def test_valid_ips():
    # Verify standard local host addresses evaluate as valid
    assert validate("127.0.0.1") is True
    # Verify the absolute maximum boundary values (255 for all bytes) pass
    assert validate("255.255.255.255") is True
    # Verify the absolute minimum boundary values (0 for all bytes) pass
    assert validate("0.0.0.0") is True
    # Verify a standard private subnet address structure passes
    assert validate("192.168.1.1") is True

def test_invalid_ip_range():
    # Verify that a first byte exceeding 255 is caught and rejected
    assert validate("275.3.6.28") is False
    # Verify that a first byte exactly at 256 is caught and rejected
    assert validate("256.1.1.1") is False
    # Verify that a middle byte exceeding the 255 threshold is rejected
    assert validate("1.256.1.1") is False
    # Verify that the final byte exceeding the 255 threshold is rejected
    assert validate("1.1.1.300") is False

def test_invalid_ip_format():
    # Verify that an incomplete address with only 3 segments fails
    assert validate("1.1.1") is False
    # Verify that an oversized address with 5 segments fails
    assert validate("1.1.1.1.1") is False
    # Verify that a completely non-numeric text string fails
    assert validate("cat") is False
    # Verify that mixed alphanumeric segments containing letters fail
    assert validate("192.168.1.abc") is False
