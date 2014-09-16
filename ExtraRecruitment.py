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
if os.path.exists('%s/Users/JingqianLi/Desktop/serach_result/.DS_Store' %os.getcwd()):
	os.remove('%s/Users/JingqianLi/Desktop/search_result/.DS_Store' %os.getcwd())  
'''

L = os.listdir('/Users/JingqianLi/Desktop/search_result')	 # put all the xml file names into an array
del L[0]  # delete the frist element because I couldn't remove .DS_Store 

outputFile = open('extraRecruitment.xml', 'a')
for i in xrange(len(L)):
	soup = BeautifulSoup(open("/Users/JingqianLi/Desktop/search_result/%s" %L[i]))  
	outputFile.write(soup.eligibility.prettify())
	outputFile.write('\n'*3)

outputFile.close()  # python shut down after the i increased to nearly 1000


