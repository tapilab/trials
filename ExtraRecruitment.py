#!/usr/bin/python
# -*- coding: utf-8 -*-  	 	

from bs4 import BeautifulSoup
import os
import sys

print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

'''
if os.path.exists("%s/Users/JingqianLi/Documents/serach_result/.DS_Store"):
	os.remove("%s/Users/JingqianLi/Desktop/search_result/.DS_Store")  
'''

L = os.listdir('/Users/JingqianLi/Documents/Courses/Trials/search_result')	 # put all the xml file names into an array
#del L[0]  # delete the frist element because I couldn't remove .DS_Store 

processedFile = 0

outputFile = open('extraRecruitment2.xml', 'a')
outputFile.write('<Trials>')
outputFile.write('\n')
outputFile.write('<experiment>')
outputFile.write('\n')

for i in xrange(len(L)):
	soup = BeautifulSoup(open("/Users/JingqianLi/Documents/Courses/Trials/search_result/%s" %L[i])) 
	 
	if soup.eligibility == None:
		processedFile += 1

	else:
		count = 0
		while (soup.find_all()[count] != soup.id_info):
			count += 1
		while (soup.find_all()[count] != soup.eligibility):
			outputFile.write(soup.find_all()[count].prettify())
			count += 1
		outputFile.write(soup.eligibility.prettify())
		outputFile.write('\n'*3)
		print i+1
		processedFile += 1

outputFile.write('</experiment>')
outputFile.write('\n')
outputFile.write('</Trials>')

outputFile.close()  

print "Files have been processed: %s" %processedFile


