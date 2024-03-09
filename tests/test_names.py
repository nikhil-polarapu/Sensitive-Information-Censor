from censoror import censor, readFile
import pytest

def test_maskedNameTrue():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    value = "Robert Benson"
    data = readFile('output/1..censored')
    assert False if value in data else True

def test_maskedNameFalse():
    censor('tmp/1.', False, True, True, True, 'output/', 'stats')
    value = "Robert Benson"
    data = readFile('output/1..censored')
    assert True if value in data else False