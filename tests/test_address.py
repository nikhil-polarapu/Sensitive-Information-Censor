from censoror import censor, readFile
import pytest

def test_maskedDateTrue():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    value = "Houston"
    data = readFile('output/1..censored')
    assert False if value in data else True

def test_maskedDateFalse():
    censor('tmp/1.', True, True, True, False, 'output/', 'stats')
    value = "Houston"
    data = readFile('output/1..censored')
    assert True if value in data else False