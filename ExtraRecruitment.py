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

L = os.listdir('/Users/JingqianLi/Documents/Courses/Trials/search_result2')	 # put all the xml file names into an array
#del L[0]  # delete the frist element because I couldn't remove .DS_Store 

processedFile = 0

outputFile = open('new.xml', 'a')
for i in xrange(len(L)):
	soup = BeautifulSoup(open("/Users/JingqianLi/Documents/Courses/Trials/search_result2/%s" %L[i]))  
	if soup.eligibility == None:
		processedFile += 1
	else: 
		outputFile.write(soup.id_info.prettify())
		outputFile.write(soup.brief_title.prettify())
		outputFile.write(soup.official_title.prettify())
		outputFile.write(soup.sponsors.prettify())
		outputFile.write(soup.source.prettify())
		outputFile.write(soup.oversight_info.prettify())
		outputFile.write(soup.brief_summary.prettify())
		outputFile.write(soup.detailed_description.prettify())
		outputFile.write(soup.overall_status.prettify())
		outputFile.write(soup.start_date.prettify())
		outputFile.write(soup.phase.prettify())
		outputFile.write(soup.study_type.prettify())
		outputFile.write(soup.study_design.prettify())
		outputFile.write(soup.enrollment.prettify())
		for condition in soup.find_all('condition'):     # trying to write all the <condition> notes
			outputFile.write(condition)
		outputFile.write(soup.eligibility.prettify())
		outputFile.write('\n'*3)
		print i
		processedFile += 1

outputFile.close()  

print "Files have been processed: %s" %processedFile


