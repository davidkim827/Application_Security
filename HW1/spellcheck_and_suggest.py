#!/usr/bin/env python3

"""This module was created in order to take only text (.txt) file(s),
   parse the text file so that only unique words are checked for,
   pass the list of unique words into a spell checking library, and
   print out the results of misspelled words and a list of suggestions for
   the mispelled words. If spellchecker library doesn't exist, then this program
   installs it for the user using the subprocess module which calls upon the pip module
   to install the pyspellchecker module."""

import subprocess
import argparse
import re
import sys

PUNCTUATION_LIST = [i for i in range(33, 127) if i != 39 and not chr(i).isalpha()]

def parse_file():
    """returns filename input to command line by user"""
    parser = argparse.ArgumentParser(description='Spellchecker for text file')
    parser.add_argument('-f', '--file', help='Specify a .txt file')
    args = parser.parse_known_args()
    if len(args[1]) < 1:
        sys.exit('\nText file not specified\n')
    elif len(args[1]) > 1:
        sys.exit('\nOnly one text file at a time supported\n')
    elif ".txt" not in args[1][0]:
        sys.exit('\nPlease input a .txt file\n')
    text_file = args[1]
    return text_file[0]

def read_text_file(text_file):
    """reads in the textFile and returns a list of all the unique words in the
       textFile to spellcheck"""
    return_list = []
    with open(text_file, 'r') as text:
        text = text.readlines()
        for line in text:
            line = re.split("[/ ]", line)
            for word in line:
                if word.isalpha():
                    return_list.append(word.strip().lower())
                else:
                    for char in word:
                        if ord(char) in PUNCTUATION_LIST:
                            word = word.replace(char, "")
                    if word.strip() == "":
                        continue
                    return_list.append(word.strip().lower())
    return list(set(return_list))

def check_spelling(word_list):
    """#returns a dictionary that contains the possible misspelled
        word and suggestions"""
    try:
        from spellchecker import SpellChecker
    except ModuleNotFoundError as _:
        while 1:
            choice = input("Fixing '{}' for you by installing SpellChecker.\n \
                   do you agree? [Y/N]\n".format(_))
            if choice.lower() == "n":
                sys.exit(0)
            elif choice.lower() == "y":
                subprocess.call("pip install pyspellchecker")
                from spellchecker import SpellChecker
                break
            else:
                print("Not a valid choice.")
    spell = SpellChecker(distance=1)
    misspelled = spell.unknown(word_list)
    misspelled_dict = {}
    for word in misspelled:
        misspelled_dict[word] = spell.candidates(word)
    print("\nWord :: Suggestions\n")
    for key, value in misspelled_dict.items():
        print(f"{key} :: {value}")
    print()

def main():
    """main function to run the program"""
    file_name = parse_file()
    unique_words_list = read_text_file(file_name)
    print()
    check_spelling(unique_words_list)
if __name__ == '__main__':
    main()
