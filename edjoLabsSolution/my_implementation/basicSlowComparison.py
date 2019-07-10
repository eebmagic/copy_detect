'''
NOTES:
	This code will generate image signatures for the the Directory_PATH folder and compare all of them
	This code DOES NOT record the signatures or compares them with old records
'''


from tqdm import tqdm
import time
import os
import json

import numpy as np
from image_match.goldberg import ImageSignature
gis = ImageSignature()

FULL_START = time.time()

################################################################################
### GET INPUT DIRECTORY ###

Directory_PATH = input("Drag folder here: ").strip()
# Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages"
# Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/testImages"

if not Directory_PATH.endswith('/'):
	Directory_PATH += '/'
print(Directory_PATH)

### GET FILENAMES FROM DIRECTORY ###
files = os.listdir(Directory_PATH)
fullFilePaths = []
fileNames = {}
acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']
for name in files:
	if os.path.splitext(name)[1] not in acceptableExtensions:
		pass
	else:
		fullFilePaths.append(Directory_PATH + name)
		fileNames[Directory_PATH + name] = name


################################################################################
### GENERATE NEW IMAGE SIGNATURES ###
DATA = {}
signature_startTime = time.time()
print("Generating image signatures...")

for imagePath in tqdm(fullFilePaths):
	SIG = gis.generate_signature(imagePath)
	DATA[imagePath] = SIG

print(f"Finished Generating Signatures: {time.time() - signature_startTime}")




################################################################################
### COMPARE DATA ###
print(f"\nImages: {fileNames.values()}\n")
matches = []								#record of matches to avoid double check
alreadyChecked = []
nameMatches = []
lengths = [len(name) for name in fileNames.values()]		#length of file names for output format
checkCount = 0

#########################
SIMLAR_THRESH = 0.5    ##
#########################

comparison_startTime = time.time()
for baseIndex, baseImagePATH in enumerate(fullFilePaths):
	for testIndex, testImagePATH in enumerate(fullFilePaths):
		if baseIndex != testIndex:
			if set([baseImagePATH, testImagePATH]) not in alreadyChecked:

				compareStart = time.time()
				difference = gis.normalized_distance(DATA[baseImagePATH], DATA[testImagePATH])
				print(f"{fileNames[baseImagePATH]} {' ' * (max(lengths) - len(fileNames[baseImagePATH]))} {fileNames[testImagePATH]} {' ' * (max(lengths) - len(fileNames[testImagePATH]))} | {round(difference, 3)}", end='')
				if difference < SIMLAR_THRESH:
					matches.append(set([baseImagePATH, testImagePATH]))
					nameMatches.append([fileNames[baseImagePATH], fileNames[testImagePATH]])
					print("  -  MATCH FOUND")
				else:
					print("")
				alreadyChecked.append(set([baseImagePATH, testImagePATH]))
				checkCount += 1
				


print(f"\nMade {len(alreadyChecked)} comparisons")
print(f"\n{len(matches)} matches found.")
print(f"Finished comparisons in: {time.time() - comparison_startTime}\n")


### RESULTS ###
for match in nameMatches:
	print(match[0], match[1])
	
	## Optionally open matched images
	# for file in match:
	# 	os.system("open " + file)

print(f"\nFull Time: {time.time() - FULL_START}")

