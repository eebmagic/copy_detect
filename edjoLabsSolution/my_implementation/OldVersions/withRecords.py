'''
NOTE:
	This code will generate image signatures for Directory_PATH and store the signatures.
'''

from tqdm import tqdm
import time
import os
import json

import numpy as np
from image_match.goldberg import ImageSignature
gis = ImageSignature()

################################################################################
### FUNCTIONS ###

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



################################################################################



FULL_START = time.time()

dataDir_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/datafiles/"
rosterFile_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/datafiles/_roster.json"

################################################################################
### GET INPUT DIRECTORY ###
# Directory_PATH = input("Drag folder here: ").strip()
Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages"
Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/testImages"

if not Directory_PATH.endswith('/'):
	Directory_PATH += '/'
print(Directory_PATH)

### GET FILENAMES FROM DIRECTORY ###
files = os.listdir(Directory_PATH)
files = removeNonimages(files)
fullFilePaths = [Directory_PATH + file for file in files]
fileNames = {}
for i in range(len(files)):
	fileNames[fullFilePaths[i]] = files[i]


################################################################################
### Check Directory and filecount in _roster.json ###
## If matches load the {time}.json file ##
with open(rosterFile_PATH) as rosterFile:
	lastRecord = json.load(rosterFile)

if Directory_PATH in lastRecord:
	with open(dataDir_PATH + lastRecord[Directory_PATH]['time'] + '.json') as jsonDataFile:
		storedDATA = json.load(jsonDataFile)
		DATA = {}
		for key, LIST in storedDATA.items():
			DATA[key] = np.asarray(LIST)

else:
	## If not identical in _roster.json, make new data ##
	### GENERATE NEW IMAGE SIGNATURES ###
	DATA = {}
	signature_startTime = time.time()
	print("Generating image signatures...")

	for imagePath in tqdm(fullFilePaths):
		SIG = gis.generate_signature(imagePath)
		DATA[imagePath] = SIG

	print(f"Finished Generating Signatures: {time.time() - signature_startTime}")


	## store sigs to own .json ##
	fileTime = str(time.time())
	newFile_PATH = dataDir_PATH + str(fileTime) + '.json'
	os.system(f"touch {newFile_PATH}")

	#Convert arrays to lists
	writeDATA = {}
	for key, val in DATA.items():
		writeDATA[key] = val.tolist()

	with open(newFile_PATH, 'w') as sigRecordFile:
		json.dump(writeDATA, sigRecordFile)
		print(f"New record file for this direcoty has been created ({str(fileTime) + '.json'})")

	# keep record in _roster.json
	with open(rosterFile_PATH) as rosterFile:
		record = json.load(rosterFile)
	record[Directory_PATH] = {'time':fileTime, 'filenames':list(fileNames.values())} ### NOTE: Possibly change this to a checksum ???

	with open(rosterFile_PATH, 'w') as rosterFile:
		json.dump(record, rosterFile)
		print(f"Roster has been updated")



################################################################################
### COMPARE DATA ###
print(f"\nImages: {fileNames.values()}\n")
matches = []								#record of matches to avoid double check
alreadyChecked = []
nameMatches = []
lengths = [len(name) for name in fileNames.values()]		#length of file names for output format
similarityThresh = 0.5

comparison_startTime = time.time()
for baseIndex, baseImagePATH in enumerate(fullFilePaths):
	for testIndex, testImagePATH in enumerate(fullFilePaths):
		if baseIndex != testIndex:
			if set([baseImagePATH, testImagePATH]) not in alreadyChecked:

				compareStart = time.time()
				difference = gis.normalized_distance(DATA[baseImagePATH], DATA[testImagePATH])
				print(f"{fileNames[baseImagePATH]} {' ' * (max(lengths) - len(fileNames[baseImagePATH]))} {fileNames[testImagePATH]} {' ' * (max(lengths) - len(fileNames[testImagePATH]))} | {round(difference, 3)}", end='')
				if difference < similarityThresh:
					matches.append(set([baseImagePATH, testImagePATH]))
					nameMatches.append([fileNames[baseImagePATH], fileNames[testImagePATH]])
					print("  -  MATCH FOUND")
				else:
					print("")
				alreadyChecked.append(set([baseImagePATH, testImagePATH]))
				


print(f"\n{len(matches)} matches found.")
print(f"Finished in: {time.time() - comparison_startTime}\n")


### RESULTS ###
for match in nameMatches:
	print(match[0], match[1])
	# for file in match:
	# 	os.system("open " + file)

print(f"Full Time: {time.time() - FULL_START}")