import os
import sys

from stat import *

#print(sys.argv)

def checkFiles(path):
	for file in os.listdir(path):
		newPath = os.path.join(path,file)
		mode = os.stat(newPath).st_mode
		
		if(S_ISDIR(mode)):
			checkFiles(newPath)
		else:
			filename, extension = os.path.splitext(file)
			if(extension == ".rb"):
				#print(file)
				with open(newPath, "r") as rubyFile:
					data = rubyFile.readlines()
					print(data)
	

checkFiles(sys.argv[1])
