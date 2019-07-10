'''
NOTE:
	THIS IS A COMPLETE REWRITE
	This code will generate image signatures for Directory_PATH and store the signatures.
'''

from tqdm import tqdm
import time
import os
from pathlib import Path
import json
import itertools
import sys

import numpy as np
from image_match.goldberg import ImageSignature
gis = ImageSignature()

################################################################################
### CLI OPTIONS ###
cli_dirInput = ['-d', '--dir', '--directory']
cli_fullPrint = ['-a', '--all', '--full-output']
accetable_cli_options = cli_dirInput + cli_fullPrint

if len(sys.argv[:]) > 1 and sys.argv[1] and sys.argv[1] not in accetable_cli_options:
	quit(f"###ERROR: No such option: '{sys.argv[1]}'")

Directory_PATH = ''
for i, val in enumerate(sys.argv):
	if val in cli_dirInput:
		Directory_PATH = sys.argv[i+1]
		print("\tSetting directory from cli input!: " + Directory_PATH)

	if val in cli_fullPrint:
		printFullOut = True
	else:
		# printFullOut = False
		printFullOut = True



################################################################################
### FUNCTIONS ###
def makeSignatures(inputImageList):
	start = time.time()
	print("Generating Signatures...")
	signatures = []
	for imageFullPATH in tqdm(inputImageList):
		signatures.append(gis.generate_signature(imageFullPATH))
	print(f"Generated {len(signatures)} signatures in {round(time.time() - start, 2)} seconds")
	return(signatures)

def removeNonimages(listInput):
	acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']

	acceptedFiles = []
	for name in listInput:
		if os.path.splitext(name)[1] not in acceptableExtensions:
			pass
		else:
			acceptedFiles.append(name)
	return(acceptedFiles)

def updateWithNewData(newestData):
	pass
################################################################################



'''				  
	STARTING HERE 
				  '''
FULL_START = time.time()

################################################################################
### CHECK FOR datafiles/ DIRECTORY ###
datafiles_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/datafiles/"
if os.path.isdir(Path(datafiles_PATH)) == False:
	print("No datafiles/ directory was found.")
	os.system(f"mkdir -p {datafiles_PATH}")
	print("new datfiles/ direcotyr has been generated.")

### CHECK FOR ROSTER FILE ###
roster_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/datafiles/_roster.json"
if os.path.isfile(Path(roster_PATH)) == False:
	print("No _roster.json file was found.")
	os.system("touch " + roster_PATH)
	os.system("echo '{}' >> " + roster_PATH)
	print("New _roster.json file was generated.")


################################################################################
### GET INPUT FOLDER ###
validInputDir = False
# if len(sys.argv) > 1:
# 	if os.path.isdir(Path(sys.argv[-1])):
# 		Directory_PATH = sys.argv[-1]
# 		validInputDir = True

while not validInputDir:
	if not Directory_PATH:
		print("INPUT: " + Directory_PATH)
		Directory_PATH = input("Drag folder here: ").strip()
		# Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages"
		# Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/testImages"

	if Directory_PATH[-1] != '/':
		Directory_PATH += '/'
	if '~' in Directory_PATH:
		Directory_PATH = Directory_PATH.replace('~', str(Path.home()))

	#test Directory_PATH real folder
	if os.path.isdir(Path(Directory_PATH)) == False:
		quit(f"Invalid Path: {Directory_PATH}")
	else:
		validInputDir = True

### GET CURRENT IMAGES ###
currentFiles = os.listdir(Directory_PATH)
currentImages = removeNonimages(currentFiles)
currentImage_PATHS = [Directory_PATH + image for image in currentImages]


################################################################################
### Check roster for Directory_PATH in roster ###
with open(roster_PATH) as file:
	rosterData = json.load(file)
	sigRecordFound = Directory_PATH in rosterData
	# print(rosterData)


################################################################################
### If Directory_PATH not in roster ###
if not sigRecordFound:
	print("No record for inputDir found.")
	## Make all new signatures ##
	newImage_PATHS = currentImage_PATHS[:]
	SIGS = makeSignatures(currentImage_PATHS)
	DATA = {}

	for i, imagePATH in enumerate(currentImage_PATHS):
		# print(f"DATA: {type(DATA)}")
		# print(f"imagePATH: {imagePATH}")
		# print(f"SIGS: {type(SIGS)}")
		# print(f"i: {i} {type(i)}")
		DATA[imagePATH] = SIGS[i]


################################################################################
### If Directory_PATH is in roster ###
elif sigRecordFound:
	print("A record for inputDir was found.")
	rosterDirData = rosterData[Directory_PATH]
	# oldImages = set(rosterDirData['filenames'])
	sigFile_PATH = datafiles_PATH + rosterDirData['time'] + '.json'
	if os.path.isfile(sigFile_PATH) == True:
		print("Signature file was found.")
		sigFileFound = True
		with open(sigFile_PATH) as file:
			DATA = json.load(file)
			print("Loaded old signatures")
			oldImage_PATHS = []
			oldImages = []
			for path in DATA:
				oldImage_PATHS.append(path)
				oldImages.append(path[len(Directory_PATH):])
	else:
		print("Signature file was NOT found.")
		sigFileFound = False

	### If complete match ###
	if set(currentImage_PATHS) == set(oldImage_PATHS) and sigFileFound:
		exactMatch = True
		print("Complete match found in recods.")
		quit("### QUITING: No new images to compare.")


	### If difference in records ###
	elif set(currentImages) != set(oldImages) and sigFileFound:
		print("Differences between current dir and record.")
		exactMatch = False
		newImage_PATHS = [Directory_PATH + image for image in currentImages if image not in oldImages]
		newSigs = makeSignatures(newImage_PATHS)
		newData = {}
		for i, imagePath in enumerate(newImage_PATHS):
			newData[imagePath] = newSigs[i]

		with open(sigFile_PATH) as file:
			DATA = json.load(file)
			print("Loaded old signatures.")

		## Update DATA with newData from new signatures ##
		print("Updating DATA with newData.")
		DATA.update(newData)
	else:
		exactMatch = False


	## Work with loaded signatures
	removedOld = False
	for PATH in DATA:
		#Remove extra signatures
		if PATH not in currentImage_PATHS:
			del(DATA[PATH])
			removedOld = True
		#Convert signatures to nparrays
		elif type(DATA[PATH]) == list:
			old = DATA[PATH]
			new = np.asarray(DATA[PATH])
			DATA[PATH] = new

	if removedOld:
		print("Removed some signatures for images that no longer exist in the directory.")

		DATA.update(newData)

# print(DATA)

################################################################################
### UPDATE DATA ### (Only if there is data changed)
if not sigRecordFound or not exactMatch:
	#Convert DATA arrays to lists
	writeDATA = {}
	for key, val in DATA.items():
		if type(val) != list:
			writeDATA[key] = val.tolist()
		else:
			writeDATA[key] = val

	#Generate new time.json file with signatures (as lists)
	fileTime = str(time.time())
	newSigFile_PATH = datafiles_PATH + fileTime + '.json'
	os.system(f"touch {newSigFile_PATH}")
	with open(newSigFile_PATH, 'w') as file:
		json.dump(writeDATA, file)
		print("New signature file for this folder has been saved.")

	#Update roster with new fileTime and filenames
	rosterData[Directory_PATH] = {"time":str(fileTime), "filenames":currentImages}
	with open(roster_PATH, 'w') as file:
		json.dump(rosterData, file)
		print("Roster data has been updated for this folder.")

	#Remove old signature file
	if sigRecordFound:
		os.system(f"rm {sigFile_PATH}")
		print("Removed old signature file for this folder.")
else:
	print("No changes to update to files.")



################################################################################
#######################
### RUN COMPARISONS ###
#######################
print("\n\n\t~~~STARTING COMPARISON~~~\n")
print(f"\nImages: {currentImages}\n")
matches = []
short = []
lengths = [len(name) for name in currentImages]		# used for lining up filenames in output to not wrap

###########################
SIMILARITY_THRESH = 0.5 ###
###########################

comparisonStartTime = time.time()

### MAKE COMPARE SETS ###
# combos = list(itertools.combinations(currentImage_PATHS, 2))  ## Make every possible combination for all pics in directory
combos = [] 					## Make tupe with every new image against all images in directory (Old & New)
for newImg in newImage_PATHS:
	for compareImg in currentImage_PATHS:
		if newImg != compareImg:
			combos.append((newImg, compareImg))

print(combos)
print("Here are all combos: ^")

### RUN COMPARE ###
for comb in combos:
	difference = gis.normalized_distance(DATA[comb[0]], DATA[comb[1]])

	nameA = comb[0][len(Directory_PATH):]
	nameB = comb[1][len(Directory_PATH):]
	fullLine = str(f"{nameA} {' ' * (max(lengths) - len(nameA))} {nameB} {' ' * (max(lengths) - len(nameB))} | {round(difference, 3)}")

	if difference < SIMILARITY_THRESH:
		matches.append(comb)
		short.append((nameA, nameB))
		print(fullLine + " - MATCH !!!")
	elif printFullOut:
		print(fullLine)

print(f"\n{len(combos)} comparisons in {round(time.time() - comparisonStartTime, 4)} secs")
print(f"Total time: {round(time.time() - FULL_START, 4)} secs")

print(f"\n\n{len(matches)} matches found: \n")
for match in matches:
	print(f"{match[0][len(Directory_PATH):]}  &  {match[1][len(Directory_PATH):]}")




