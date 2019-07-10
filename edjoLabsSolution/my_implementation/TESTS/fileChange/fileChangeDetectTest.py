import json
import os

Dir_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/TESTS/sampleDir/"
# Dir_PATH = input("Drag folder here: ").strip() + '/'
dataDir_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/TESTS/dataFiles/"


def removeNonimages(listInput):
	acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']

	output = []
	for name in listInput:
		if os.path.splitext(name)[1] not in acceptableExtensions:
			pass
		else:
			output.append(name)
	return(output)


allFiles = os.listdir(Dir_PATH)
imageFiles = removeNonimages(allFiles)

print(imageFiles)