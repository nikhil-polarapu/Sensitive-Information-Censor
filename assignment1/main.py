import glob
import spacy
import re
import sys
from warnings import filterwarnings

filterwarnings('ignore')

# Function to read data from a file
def readFile(filename):
    with open(filename, 'r') as f:
        return f.read()

# Function to write data to a file
def writeFile(filename, text):
    with open(filename, 'w') as f:
        f.write(text)

# Function to mask a string
def replaceString(string):
    char = '\u2588'
    return char * (len(string))

# Function write stats to stderr
def writeStatsStderr(statistics):
    for sublist in statistics:
        for item in sublist:
            line = ', '.join(map(str, item))
            sys.stderr.write(line + '\n')
        sys.stderr.write('\n')

# Function write stats to stdout
def writeStatsStdout(statistics):
    for sublist in statistics:
        for item in sublist:
            line = ', '.join(map(str, item))
            sys.stdout.write(line + '\n')
        sys.stdout.write('\n')

# Function to write stats to a file
def writeStatsDefault(stats, statistics):
    with open(stats, 'w') as f:
        for sublist in statistics:
            for item in sublist:
                line = ', '.join(map(str, item))
                f.write(line + '\n')
            f.write('\n')

# Function to censor the sensitive information
def censor(input, names, dates, phones, addresses, output, stats):
    nlp = spacy.load('en_core_web_md')
    files = glob.glob(input)
    statistics_1 = [['Type', 'Count'], ['Name', 0], ['Date', 0], ['Phone', 0], ['Adress', 0]]
    statistics_2 = [['File Name', 'Type', 'Count']]
    statistics_3 = [['File Name', 'Masked Value', 'Starting Index', 'Ending Index']]

    stats2 = {}
    stats3 = {}

    for file in files:
        data = readFile(file)
        doc = nlp(data)
        fileName = file.split('/')[-1]
        stats2[fileName] = {'Name': 0, 'Date': 0, 'Phone': 0, 'Address': 0}

        for ent in doc.ents:
            # Masking the names
            if(names and ent.label_ == 'PERSON'):
                data = data.replace(ent.text, replaceString(ent.text))
                statistics_1[1][1] += 1
                stats2[fileName]['Name'] += 1
                statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
            # Masking the dates
            if(dates and ent.label_ == 'DATE'):
                data = data.replace(ent.text, replaceString(ent.text))
                statistics_1[2][1] += 1
                stats2[fileName]['Date'] += 1
                statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
            # Masking the phone numbers
            if(phones):
                phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
                phone_numbers = phone_pattern.findall(data)
                for phone_number in phone_numbers:
                    start_index = data.index(phone_number)
                    end_index = start_index + len(phone_number) - 1
                    data = data.replace(phone_number, replaceString(phone_number))
                    statistics_1[3][1] += 1
                    stats2[fileName]['Phone'] += 1
                    statistics_3.append([fileName, phone_number, start_index, end_index])
                if(ent.label_ == 'PHONE'):
                    data = data.replace(ent.text, replaceString(ent.text))
                    statistics_1[3][1] += 1
                    stats2[fileName]['Phone'] += 1
                    statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
            # Masking the addresses
            if(addresses):
                if(ent.label_ == 'GPE' or ent.label_ == 'LOC'):
                    data = data.replace(ent.text, replaceString(ent.text))
                    statistics_1[4][1] += 1
                    stats2[fileName]['Address'] += 1
                    statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
        # Writing the masked output to a file
        writeFile(output+fileName+'.censored', data)

    for filename, details in stats2.items():
        for _type, count in details.items():
            statistics_2.append([filename, _type, count])
    
    statistics = [statistics_1, statistics_2, statistics_3]
    
    # Writing statistics to a file specified in the input
    if(stats == 'stderr'):
        writeStatsStderr([statistics_1, statistics_2, statistics_3])
    elif(stats == 'stdout'):
        writeStatsStdout([statistics_1, statistics_2, statistics_3])
    else:
        writeStatsDefault(stats, [statistics_1, statistics_2, statistics_3])