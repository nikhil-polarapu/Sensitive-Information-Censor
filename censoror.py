import argparse
import glob
import spacy
import en_core_web_md
import re
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

def censor(input, names, dates, phones, addresses, output, stats):
    nlp = en_core_web_md.load()
    files = glob.glob(input)
    readFiles = []
    for file in files:
        print(file)
        data = readFile(file)
        doc = nlp(data)
        for ent in doc.ents:
            if(names):
                if(ent.label_ == 'PERSON'):
                    data = data.replace(ent.text, replaceString(ent.text))
            if(dates):
                if(ent.label_ == 'DATE'):
                    data = data.replace(ent.text, replaceString(ent.text))
            if(phones):
                phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
                phone_numbers = phone_pattern.findall(data)
                for phone_number in phone_numbers:
                    data = data.replace(phone_number, replaceString(phone_number))
                if(ent.label_ == 'PHONE'):
                    data = data.replace(ent.text, replaceString(ent.text))
            if(addresses):
                if(ent.label_ == 'GPE' or ent.label_ == 'LOC'):
                    data = data.replace(ent.text, replaceString(ent.text))
        print(file.split('/')[-1])
        writeFile(output+file.split('/')[-1]+'.censored', data)

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input file directory.")
    parser.add_argument("--names", action="store_true", required=False, help="Should names be censored?")
    parser.add_argument("--dates", action="store_true", required=False, help="Should dates be censored?")
    parser.add_argument("--phones", action="store_true", required=False, help="Should phone numbers be censored?")
    parser.add_argument("--address", action="store_true", required=False, help="Should addresses be censored?")
    parser.add_argument("--output", type=str, required=True, help="Output file directory.")
    parser.add_argument("--stats", type=str, required=False, help="Input either the name of a file or special files (stderr, stdout) to write summary to.")
     
    args = parser.parse_args()

    censor(args.input, args.names, args.dates, args.phones, args.address, args.output, args.stats)

    # if(args.input):
    #     print(args.input)
    # print(args.names)
    # print(args.dates)
    # print(args.phones)
    # print(args.address)
    # if(args.output):
    #     print(args.output)
    # if(args.stats):
    #     print(args.stats)