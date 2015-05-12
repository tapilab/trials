with open('/Users/JingqianLi/Documents/Documents/Github/trials/trials/searchapp/file_path.txt','r') as fp:
	for line in fp:
		if line[:6] == "RAWDIR":
			RAWDIR = line[7:]
		elif line[:8] == "INDEXDIR":
			INDEXDIR = line[9:]
	fp.close()