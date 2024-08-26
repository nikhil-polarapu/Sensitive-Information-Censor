# Sensitive Information Censor

# Project Description

In this project we write a program that accepts plain text documents, detects sensitive information and censors them. Sensitive information includes the following values.

- Names
- Dates
- Phone Numbers
- Addresses

The program accepts input file that has the text that must be censored, along with flags for the above mentioned values. It also accepts an output flag that specifies the file to which the masked data must be written to. A stats flag is also mentioned along with the file to which the statistics of the masked values must be written to. The following input flags must be specified when running the program.

- --input (string)
- --names (boolean)
- --dates (boolean)
- --phones (boolean)
- --address (boolean)
- --output (string)
- --stats (string)

# How to install

- curl https://pyenv.run | bash
- pyenv install 3.11
- pyenv global 3.11
- pip install pipenv
- pipenv run pip install -U pip setuptools wheel
- pipenv run pip install -U spacy
- pipenv run pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.7.1/en_core_web_md-3.7.1-py3-none-any.whl
- pipenv run pip install warning
- pipenv install pytest

## How to run

- pipenv run python censoror.py --input 'tmp/*' --names --dates --phones --address --output output/ --stats stats
- pipenv run python -m pytest

![DE Assignment1 Demo](/DE%20Assignment%201%20-%20Demo.gif)


## Functions

#### censoror.py \

- This program collects the inputs mentioned in the assignment description part and their values, and feeds them to a function that censors the sensitive information.

#### main.py \

- readFile( ) - This function takes a filename as input and reads the data from that file. It returns the data that is read from this file.

- writeFile( ) - This function takes in a filename and data as inputs. It then writes the mentioned data to this file.

- replaceString( ) - This function takes a string as input and masks it with a block character: &#9608;. It returns this masked string.

- writeStatsStderr( ) - This function takes in the statistics list as input and writes this data to the special file stderr. It does not return anything.

- writeStatsStdout( ) - This function takes in the statistics list as input and writes this data to the special file stdout. It does not return anything.

- writeStatsDefault( ) - This function takes in the statistics list and a file as inputs. It then writes this statistics data to the mentioned file. It does not return anything.

- censor( ) - This function takes in the inputs mentioned in the assignment description. It then loads the 'en_core_web_md' model from spacy. It reads the input from file argument passed. Using the 'en_core_web_md' model, it identifies values of the following categories in the data and masks them using replaceString() function. It then writes this data to the file specified as the output value.
  - name
  - date
  - phone
  - address

## Statistics Considered

The following statistics are written to the statistics file.
- **Type, Count**
  The type of the masked item and its count across all the input files.

- **File Name, Type, Count**
  The type of the masked item and its count for each input file.

- **File Name, Masked Value, Starting Index, Ending Index**
  The masked value with its beginning and end indices for each file.

The statistics are written to one of the following files based on the stats argument.

- stderr
- stdout
- \<file mentioned\>

## Bugs and Assumptions

The following assumptions were made:
  
- Phone numbers are always of the format (555)555-5555 or 555-555-5555.
- Program relies on spacy's capability to correctly identify the values.
- Since a medium model is used it may not work well for a very big dataset.
- Glob always extracts the files under a directory correctly.
- The directories given by the user are valid and they already exist.

If any page does not follow the above-mentioned assumptions then bugs related to these assumptions may be encountered.

## Testcase Discussion

- test_maskedNameTrue( ) - Testcase to check if names are masked properly when the --names flag is true.
- test_maskedNameFalse( ) - Testcase to check if names are not masked when the --names flag is false.
- test_maskedDateTrue( ) - Testcase to check if dates are masked properly when the --dates flag is true.
- test_maskedDateFalse( ) - Testcase to check if dates are not masked when the --dates flag is false.
- test_maskedPhoneTrue( ) - Testcase to check if phone numbers are masked properly when the --phones flag is true.
- test_maskedPhoneFalse( ) - Testcase to check if phone numbers are not masked when the --phones flag is false.
- test_maskedAddressTrue( ) - Testcase to check if addresses are masked properly when the --address flag is true.
- test_maskedAddressFalse( ) - Testcase to check if addresses are not masked when the --address flag is false.
- test_output( ) - Testcase to check if a proper output file is being created.
- test_statsCreation( ) - Testcase to check if a proper stats file is being created.
- test_statsColumns( ) - Testcase to check if the created stats has the correct columns.
