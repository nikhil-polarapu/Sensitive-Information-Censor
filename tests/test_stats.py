from assignment1.main import censor, readFile
import pytest
import os

# Testcase to check if a proper stats file is being created.
def test_statsCreation():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    assert True if os.path.isfile('stats') else False

# Testcase to check if the created stats has the correct columns.
def test_statsColumns():
    censor('tmp/1.', True, True, True, True, 'output/', 'stats')
    data = readFile('stats')
    vals = ['Type, Count', 'File Name, Type, Count', 'File Name, Masked Value, Starting Index, Ending Index']
    flag = 0
    for i in vals:
        if(i in data):
            flag += 1 
    assert True if flag == 3 else False

