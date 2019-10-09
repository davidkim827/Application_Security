#!/usr/bin/env python3
import subprocess
import argparse
import re
from spellchecker import SpellChecker

punctuationList = [i for i in range(33,127) if i != 39 and chr(i).isalpha() == False]

#returns filename input to command line by user
def parseFile():
	parser = argparse.ArgumentParser(description='Spellchecker for text file')
	parser.add_argument('-f', '--file', help='Specify a .txt file')
	args = parser.parse_known_args()
	if len(args[1]) < 1:
		print ('\nText file not specified\n')
		exit(1)
	elif len(args[1]) > 1:
		print('\nOnly one text file at a time supported\n')
		exit(1)
	elif ".txt" not in args[1]:
		print("\nPlease input a .txt file\n")
		exit(1)
	textFile = args[1]
	return textFile[0]

#reads in the textFile and returns a list of all the unique words in the textFile to spellcheck
def readTextFile(textFile):
    returnList = []
    with open(textFile, 'r') as text:
        text = text.readlines()
        for line in text:
            line = re.split("[/ ]",line)
            for word in line:
                if word.isalpha():
                    returnList.append(word.strip().lower())
                else:
                    for char in word:
                        if ord(char) in punctuationList:
                            word = word.replace(char,"")
                    if word.strip() == "":
                        continue
                    returnList.append(word.strip().lower())
    return list(set(returnList))

#returns a dictionary that contains the possible misspelled word and suggestions
def checkspelling(wordList):
	spell = SpellChecker(distance=1)
	misspelled = spell.unknown(wordList)
	misspelledDict = {}
	#print(type(misspelled))
	#print("Possible Misspelled Words:\n{}".format(misspelled))
	for word in misspelled:
		misspelledDict[word] = spell.candidates(word)
	print("Word : Suggestions")
	for key,value in misspelledDict.items():
		print(f"{key} :: {value}")
		

def main():
	try:
		import spellchecker
	except:
		subprocess.call("pip install pyspellchecker")
		import spellchecker

	fileName = parseFile()
	uniqueWordsList = readTextFile(fileName)
	#print(uniqueWordsList)
	print()
	
	checkspelling(uniqueWordsList)


if __name__ == '__main__': main()