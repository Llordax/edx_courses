# Import the 'shorten' function from your existing vowel-removal module (twttr.py)
from twttr import shorten

def test_lowercase():
    # Verify that lowercase vowels are correctly removed from standard words
    assert shorten("twitter") == "twttr"
    assert shorten("hello") == "hll"

def test_uppercase():
    # Verify that uppercase vowels are correctly identified and removed as well
    assert shorten("TWITTER") == "TWTTR"
    assert shorten("HELLO") == "HLL"

def test_numbers():
    # Verify that numbers are completely ignored by the filter and remain unchanged
    assert shorten("cs50") == "cs50"
    assert shorten("12345") == "12345"

def test_punctuation():
    # Verify that symbols, spaces, and punctuation marks are preserved perfectly
    assert shorten("hello, world!") == "hll, wrld!"
    # Verify that when all vowels are stripped out, only the punctuation markers remain
    assert shorten("a.e.i.o.u?") == "....?"
