#!/bin/python

import urllib2
import json
import datetime
import csv 
import time
import sys



#	This script is designed to scrape data from various facebook pages
#	It looks for comments containing certain words and saves them to a file
#
#	It takes 2 arguments:
#		1. the filename of the tagret word list
#		2. the filename of the target page list
#
#	It is dependent on a file called "userapp.json" containing the App ID and App Secret to be used



def stroll(url):

	# a helper fucntion to catch HTTP Error 500

	req = urllib2.Request(url)
	success = False
	while success is False:
		try: 
		    response = urllib2.urlopen(req)
		    if response.getcode() == 200:
			success = True
		except Exception, e:
		    print e
		    time.sleep(5)
		    
		    print "Error for URL %s: %s" % (url, datetime.datetime.now())

	return response



def url_maker(page_id, access_token):

	url_base = "https://graph.facebook.com/v2.4"
	node = "/" + page_id
	parameters = "/?access_token=%s" % access_token
	url = url_base + node + parameters

	return url



def off_the_pavement(page, word, token):

	# a function to scrape and return page data

	url = url_maker(page, token)
	response = stroll(url)
	data = json.loads(response.read())

	print json.dumps(data, indent=4, sort_keys=True)



def main():

	# reads in the app info, word list and page list

	USERAPP = "userapp.json"
	AppInfo = json.loads(open(USERAPP, 'r').read())
	
	app_id = AppInfo["App ID"]
	app_secret = AppInfo["App Secret"]
	access_token = app_id + "|" + app_secret

	WORDS = open(sys.argv[1], 'r').read().split('\n')
	WORDS.pop()
	PAGES = open(sys.argv[2], 'r').read().split('\n')
	PAGES.pop()

	# looks through each page 

	### TESTER ###

	url = url_maker('nytimes', access_token)
	response = stroll(url)
	data = json.loads(response.read())
	print json.dumps(data)

	### TESTER ###



if __name__ == "__main__":
	main()
