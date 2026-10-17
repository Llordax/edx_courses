# Import the 'count' function from your existing filler-word module (um.py)
from um import count

def test_isolated_um():
    # Verify that a single isolated "um" returns a count of 1
    assert count("um") == 1
    # Verify that multiple instances separated by a space are counted correctly
    assert count("um um") == 2
    # Verify that three independent instances are captured accurately
    assert count("um um um") == 3

def test_case_insensitive_um():
    # Verify that fully capitalized instances ("UM") are caught and counted
    assert count("UM, I don't know, UM, maybe?") == 2
    # Verify that mixed-case variations ("uM") are caught successfully
    assert count("uM, excuse me?") == 1

def test_um_with_punctuation_and_substrings():
    # Verify that an instance surrounded by commas is correctly isolated and counted
    assert count("hello, um, world") == 1
    # Verify that an instance followed immediately by a question mark passes
    assert count("um?") == 1
    # Verify that "um" embedded within other words ("yummy", "umbrella") is ignored (counts as 0)
    assert count("yummy umbrella") == 0
    # Verify that punctuation combined with embedded word variations ("drums") behaves correctly
    assert count("Instruments, um, like drums?") == 1
