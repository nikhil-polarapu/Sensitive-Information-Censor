import argparse
import glob
import spacy
import re
import sys
from warnings import filterwarnings

filterwarnings('ignore')

def readFile(filename):
    with open(filename, 'r') as f:
        return f.read()

def writeFile(filename, text):
    with open(filename, 'w') as f:
        f.write(text)

def replaceString(string):
    char = '\u2588'
    return char * (len(string))

def writeStatsStderr(statistics):
    for sublist in statistics:
        for item in sublist:
            line = ', '.join(map(str, item))
            sys.stderr.write(line + '\n')
        sys.stderr.write('\n')

def writeStatsStdout(statistics):
    for sublist in statistics:
        for item in sublist:
            line = ', '.join(map(str, item))
            sys.stdout.write(line + '\n')
        sys.stdout.write('\n')

def writeStatsDefault(stats, statistics):
    with open(stats, 'w') as f:
        for sublist in statistics:
            for item in sublist:
                line = ', '.join(map(str, item))
                f.write(line + '\n')
            f.write('\n')

def censor(input, names, dates, phones, addresses, output, stats):
    #nlp = en_core_web_md.load()
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
            if(names):
                if(ent.label_ == 'PERSON'):
                    data = data.replace(ent.text, replaceString(ent.text))
                    statistics_1[1][1] += 1
                    stats2[fileName]['Name'] += 1
                    statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
            if(dates):
                if(ent.label_ == 'DATE'):
                    data = data.replace(ent.text, replaceString(ent.text))
                    statistics_1[2][1] += 1
                    stats2[fileName]['Date'] += 1
                    statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
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
            if(addresses):
                if(ent.label_ == 'GPE' or ent.label_ == 'LOC'):
                    data = data.replace(ent.text, replaceString(ent.text))
                    statistics_1[4][1] += 1
                    stats2[fileName]['Address'] += 1
                    statistics_3.append([fileName, ent.text.replace('\n', ' '), ent.start_char, ent.end_char])
        writeFile(output+fileName+'.censored', data)

    for filename, details in stats2.items():
        for _type, count in details.items():
            statistics_2.append([filename, _type, count])
    
    statistics = [statistics_1, statistics_2, statistics_3]
    
    if(stats == 'stderr'):
        writeStatsStderr([statistics_1, statistics_2, statistics_3])
    elif(stats == 'stdout'):
        writeStatsStdout([statistics_1, statistics_2, statistics_3])
    else:
        writeStatsDefault(stats, [statistics_1, statistics_2, statistics_3])

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input file directory.")
    parser.add_argument("--names", action="store_true", required=False, help="Should names be censored?")
    parser.add_argument("--dates", action="store_true", required=False, help="Should dates be censored?")
    parser.add_argument("--phones", action="store_true", required=False, help="Should phone numbers be censored?")
    parser.add_argument("--address", action="store_true", required=False, help="Should addresses be censored?")
    parser.add_argument("--output", type=str, required=True, help="Output file directory.")
    parser.add_argument("--stats", type=str, required=True, help="Input either the name of a file or special files (stderr, stdout) to write summary to.")
     
    args = parser.parse_args()

    censor(args.input, args.names, args.dates, args.phones, args.address, args.output, args.stats)