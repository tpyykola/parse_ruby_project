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
			print(file)
	

checkFiles(sys.argv[1])
