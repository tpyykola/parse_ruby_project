import os
import sys

from stat import *

#print(sys.argv)

fileList = []
requirementsList = []

def checkFiles(path):
	global fileList
	global requirementsList

	for file in os.listdir(path):
		newPath = os.path.join(path,file)
		mode = os.stat(newPath).st_mode
		
		if(S_ISDIR(mode)):
			checkFiles(newPath)
		else:
			filename, extension = os.path.splitext(file)
			if(extension == ".rb"):
				pathAndFile = [newPath.strip(sys.argv[1]), file] 
				fileList.append(pathAndFile)
				#print(file)
				with open(newPath, "r") as rubyFile:
					data = rubyFile.readlines()
				#print(data)

				needle = "require"
				for line in data:
					#print(line)
					if(line.startswith(needle)):
						#print(line)
						requiredFile = line.strip((needle+" "))
						# poistetaan rivin vaihto ja hipsut
						requiredFile = requiredFile[1:-2]
						requirementsList.append(requiredFile)	
						resultLine = newPath.strip(sys.argv[1]) + ":" + requiredFile
						#print(resultLine)
						
	


checkFiles(sys.argv[1])

#print(requirementsList)
