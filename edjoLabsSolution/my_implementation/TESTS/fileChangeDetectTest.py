import json
import os

Dir_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/TESTS/fileChange/sampleDir/"
# Dir_PATH = input("Drag folder here: ").strip() + '/'
dataDir_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/TESTS/fileChange/dataFiles/record.json"


def removeNonimages(listInput):
	acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']

	output = []
	for name in listInput:
		if os.path.splitext(name)[1] not in acceptableExtensions:
			pass
		else:
			output.append(name)
	return(output)

def getOldDataDict(jsonPath):
	with open(jsonPath) as file:
		return(json.load(file))

def saveNewDataDict(inputData, jsonPath):
	with open(jsonPath, 'w') as file:
		json.dump(inputData, file)

def getNewFiles(folderPath, jsonRecordPath):
	currentFiles = os.listdir(folderPath)
	currentImages = removeNonimages(currentFiles)

	oldData = getOldDataDict(jsonRecordPath)
	oldImages = oldData[folderPath]

	added = [image for image in currentImages if image not in oldImages]

	return(added)

def updateRecord(folderPath, jsonRecordPath):
	currentFiles = os.listdir(folderPath)
	currentImages = removeNonimages(currentFiles)

	oldData = getOldDataDict(jsonRecordPath)
	oldData[folderPath] = currentImages

	with open(jsonRecordPath, 'w') as file:
		json.dump(oldData, file)



print(f"New Images: {getNewFiles(Dir_PATH, dataDir_PATH)}")
updateRecord(Dir_PATH, dataDir_PATH); print("Updated record file.")
