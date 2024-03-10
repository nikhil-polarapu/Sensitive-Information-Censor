from assignment1.main import censor, readFile
import pytest

# Testcase to check if names are masked properly when the --names flag is true.
def test_maskedNameTrue():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    value = "Robert Benson"
    data = readFile('output/1..censored')
    assert False if value in data else True

# Testcase to check if names are not masked when the --names flag is false.
def test_maskedNameFalse():
    censor('tmp/1.', False, True, True, True, 'output/', 'stats')
    value = "Robert Benson"
    data = readFile('output/1..censored')
    assert True if value in data else False