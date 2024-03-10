from assignment1.main import censor, readFile
import pytest

# Testcase to check if dates are masked properly when the --dates flag is true.
def test_maskedDateTrue():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    value = "11 May 2001"
    data = readFile('output/1..censored')
    assert False if value in data else True

# Testcase to check if dates are not masked when the --dates flag is false.
def test_maskedDateFalse():
    censor('tmp/1.', True, False, True, True, 'output/', 'stats')
    value = "11 May 2001"
    data = readFile('output/1..censored')
    assert True if value in data else False