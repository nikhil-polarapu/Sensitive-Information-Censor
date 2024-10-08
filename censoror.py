import argparse
import assignment1.main as mainFunction

# Code to take input from the user
if(__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input file directory.")
    parser.add_argument("--names", action="store_true", required=False, help="Should names be censored?")
    parser.add_argument("--dates", action="store_true", required=False, help="Should dates be censored?")
    parser.add_argument("--phones", action="store_true", required=False, help="Should phone numbers be censored?")
    parser.add_argument("--address", action="store_true", required=False, help="Should addresses be censored?")
    parser.add_argument("--output", type=str, required=True, help="Output file directory.")
    parser.add_argument("--stats", type=str, required=True, help="Input either the name of a file or special files (stderr, stdout) to write the summary to.")
     
    args = parser.parse_args()

    # Calling censor function to mask sensitive information
    mainFunction.censor(args.input, args.names, args.dates, args.phones, args.address, args.output, args.stats)