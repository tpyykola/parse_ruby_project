import os
import sys

from stat import *

#print(sys.argv)

sourcefileList = []
fileList = []
pathList = []
requirementsList = []

def checkFiles(path):
	global sourcefileList
	global fileList
	global pathList
	global requirementsList

	print("Searching path: " + path)

	for file in os.listdir(path):
		newPath = os.path.join(path,file)
		mode = os.stat(newPath).st_mode
		
		if(S_ISDIR(mode)):
			checkFiles(newPath)
		else:
			filename, extension = os.path.splitext(file)
			if(extension == ".rb"):
				pathList.append(newPath)
				fileList.append(os.path.join(path,file))
				#print(file)

				with open(newPath, "r") as rubyFile:
					data = rubyFile.readlines()
				#print(data)

				needle = "require"	#keyword for depencies
				for line in data:
					#print(line)
					if(line.startswith(needle)):
						#print(line)
						requiredFile = line.strip((needle+" "))

						# removing quotes and EOL
						requiredFile = requiredFile[1:-2]

						requirementsList.append(requiredFile)
						sourcefileList.append(newPath)
						
				rubyFile.close()


checkFiles(sys.argv[1])

#print(fileList)
#['../test/omniauth-twitter/lib/omniauth-twitter/version.rb', '../test/omniauth-twitter/lib/omniauth-twitter.rb', '../test/omniauth-twitter/lib/omniauth/strategies/twitter.rb', '../test/omniauth-twitter/spec/spec_helper.rb', '../test/omniauth-twitter/spec/omniauth/strategies/twitter_spec.rb']

#print(pathList)
#['../test/omniauth-twitter/lib/omniauth-twitter/version.rb', '../test/omniauth-twitter/lib/omniauth-twitter.rb', '../test/omniauth-twitter/lib/omniauth/strategies/twitter.rb', '../test/omniauth-twitter/spec/spec_helper.rb', '../test/omniauth-twitter/spec/omniauth/strategies/twitter_spec.rb']


#print(requirementsList)
#['omniauth-twitter/version', 'omniauth/strategies/twitter', 'omniauth-oauth', 'json', 'simplecov', 'rspec', 'rack/test', 'webmock/rspec', 'omniauth', 'omniauth-twitter', 'spec_helper']


internalRequirements = []
externalRequirements = []
h=0	#id for sourcefileList
for requirement in requirementsList:
	value = requirement+".rb"
	#print(value)
	i=0
	index = -1
	for file in fileList:
		if(value in file):
			index = i
		i=i+1
			
	if(index == -1):
		externalRequirements.append(requirement + ":require_external")
	else:
		internalRequirements.append(sourcefileList[h].strip(sys.argv[1]) + ":" + pathList[index].strip(sys.argv[1]) + ":require_internal")

	h=h+1

#print(internalRequirements)
#print(externalRequirements)

output = open("sample-ruby-project_internal_deps.list", "w")

for line in internalRequirements:
	output.write(line)
	output.write("\n")

output.close()
