from assignment1.main import censor, readFile
import pytest

# Testcase to check if addresses are masked properly when the --address flag is true.
def test_maskedAddressTrue():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    value = "Houston"
    data = readFile('output/1..censored')
    assert False if value in data else True

# Testcase to check if addresses are not masked when the --address flag is false.
def test_maskedAddressFalse():
    censor('tmp/1.', True, True, True, False, 'output/', 'stats')
    value = "Houston"
    data = readFile('output/1..censored')
    assert True if value in data else False