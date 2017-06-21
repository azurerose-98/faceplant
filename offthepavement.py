#!/bin/python

import urllib2
import json
import datetime
import csv 
import time



#	This script is designed to scrape data from various facebook pages
#	It looks for comments containing certain words and saves them to a file
#
#	It takes 2 arguments:
#		1. the filename of the tagret word list
#		2. the filename of the target page list



def stroll(url):

	# a helper fucntion to catch HTTP Error 500



def off_the_pavement(page, word):

	# a function to scrape and return page data



def main():

	# reads in word list and page list

	WORDS = open(sys.argv[1], 'r').read().split('\n')
	WORDS.pop()
	PAGES = open(sys.argv[2], 'r').read().split('\n')
	PAGES.pop()



if __name__ == "__main__":
	main()
