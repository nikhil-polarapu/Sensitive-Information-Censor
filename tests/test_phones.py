from censoror import censor, readFile
import pytest

def test_maskedPhoneTrue():
    censor('tmp/8.', True, True, True, True, 'output/', 'stats')
    value = "713-588-5176"
    data = readFile('output/8..censored')
    assert False if value in data else True

def test_maskedPhoneFalse():
    censor('tmp/8.', True, True, False, True, 'output/', 'stats')
    value = "713-588-5176"
    data = readFile('output/8..censored')
    assert True if value in data else False