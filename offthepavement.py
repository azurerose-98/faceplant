#!/bin/python

import urllib2
import json
import datetime
import csv 
import time
import sys
import copy
import codecs
import unicodedata



#	This script is designed to scrape data from various facebook pages
#	It looks for comments containing certain words and saves them to a file
#
#	It takes 3 arguments:
#		1. the filename of the tagret word list
#		2. the filename of the target page list
#		3. the output path to dump the scraped data
#
#	It is dependent on a file called "userapp.json" containing the App ID and App Secret to be used



# initializes globally defined variables

WORDS = open(sys.argv[1], 'r').read().split('\n')
WORDS.pop()
PAGES = open(sys.argv[2], 'r').read().split('\n')
PAGES.pop()
OUTPUT_PATH = sys.argv[3]

json_fps = {}
text_fps = {}



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



def check(rawtext, n_words):

        # checks to see if text contains ONLY ONE relevant word 

        text = ''.join(rawtext.splitlines())
        split_text = text.split()

        return_string = ''
        return_word = ''

        found = False
        double = False

        for word in n_words:

                if word in split_text:
                        if found == False:
                                return_word = word
                                found = True
                        elif found == True and double == False:
                                double = True
                        else:
                                pass

                else:
                        pass

        if found == True and double == False:
                return_string = copy.deepcopy(text) + '\n' + copy.deepcopy(return_word)
        else:
                return_string = '\nFALSE'

        return return_string



def url_maker(page_id, access_token, num):

	url_base = "https://graph.facebook.com/v2.4"
	node = "/" + page_id + "/feed"
	parameters = "/?fields=message,created_time,id,likes,comments.limit(100).summary(true),shares&limit=%s&access_token=%s" % (num, access_token)
	url = url_base + node + parameters

	return url



def off_the_pavement(page, token):

	# a function to scrape and return page data

	print page + " START"

	NUM_STATUSES = 100

	url = url_maker(page, token, NUM_STATUSES)
        response = stroll(url)
        data = json.loads(response.read())['data']

	for post in data:

        	comments = post['comments']['data']	

		for comment in comments:

			text = comment['message']
			return_list = check(text, WORDS)

			print text
				
			text_str = return_list[0]
                        r_word = str(return_list[1])

                        if text_str != '':

                                json_fps[r_word].write(comment)
                                text_fps[r_word].write(unicode(text_str + '\n'))

	print page + " END"



def main():

	# reads in the app info, word list and page list

	USERAPP = "userapp.json"
	AppInfo = json.loads(open(USERAPP, 'r').read())
	
	app_id = AppInfo["App ID"]
	app_secret = AppInfo["App Secret"]
	access_token = app_id + "|" + app_secret

	# initializes global counter dicts

	for word in WORDS:

		path = OUTPUT_PATH + word + '.json'
		path2 = OUTPUT_PATH + word + '.txt'

		json_fps[copy.deepcopy(word)] = open(path, 'w')
		text_fps[copy.deepcopy(word)] = codecs.open(path2, 'w', encoding="utf-8")

	# looks through each page 

	for PAGE in PAGES:

		off_the_pavement(PAGE, access_token)

        for word in WORDS:
		
                json_fps[word].close()
		text_fps[word].close()



if __name__ == "__main__":
	main()
