'''
 coding: utf-8
'''

from bs4 import BeautifulSoup
import os
import sys

print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

'''
if os.path.exists("%s/Users/JingqianLi/Desktop/serach_result/.DS_Store"):
	os.remove("%s/Users/JingqianLi/Desktop/search_result/.DS_Store")  
'''

L = os.listdir('/Users/JingqianLi/Desktop/search_result')	 # put all the xml file names into an array
del L[0]  # delete the frist element because I couldn't remove .DS_Store 

processedFile = 0

outputFile = open('extraRecruitment.xml', 'a')
for i in xrange(len(L)):
	soup = BeautifulSoup(open("/Users/JingqianLi/Desktop/search_result/%s" %L[i]))  
	if soup.eligibility == None:
		processedFile += 1
	else:
		outputFile.write(soup.eligibility.prettify())
		outputFile.write('\n'*3)
		print i
		processedFile += 1

outputFile.close()  # python shut down after the i increased to nearly 1000

print "Files have been processed: %s" %processedFile


