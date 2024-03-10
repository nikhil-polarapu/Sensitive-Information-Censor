from assignment1.main import censor, readFile
import pytest
import os

# Testcase to check if a proper output file is being created.
def test_output():
    censor('tmp/8.', True, True, True, True, 'output/', 'stats')
    assert True if os.path.isfile('output/8..censored') else False
