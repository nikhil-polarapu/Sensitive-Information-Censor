from censoror import censor, readFile
import pytest
import os

def test_output():
    censor('tmp/8.', True, True, True, True, 'output/', 'stats')
    assert True if os.path.isfile('output/8..censored') else False
