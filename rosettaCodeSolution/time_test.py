from PIL import Image
import os
import time
from tqdm import tqdm
FULLSTART = time.time()

shortenFactor = 50

def shorten(fullData, factor):
	shortOutput = []
	indexes = [i*factor for i in range(int(len(fullData)/factor))]
	for ind in indexes:
		shortOutput.append(fullData[ind])

	return shortOutput


def return_percent(inputOne, inputTwo):
	global shortenFactor
	funcStart = time.time()

	# assert i1.mode == i2.mode, "Different kinds of images."
	assert len(inputOne) == len(inputTwo), "Different sizes."
	
	# print(f"Got data: {time.time() - funcStart}")

	pairs = zip(inputOne, inputTwo)
	dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	# print(f"Made comparison: {time.time() - funcStart}")

	ncomponents = (len(inputOne) * 3) #/ shortenFactor
	percent = (dif / 255.0 * 100) / ncomponents
	return int(percent)


########################################################################
##### MAIN #####

# Directory_PATH = input("Drag folder here: ").strip()
Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages" #For testing purposes
# Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/testImages" #For testing purposes

### Make filename list ###
files = os.listdir(Directory_PATH)
acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']
for name in files:
	if os.path.splitext(name)[1] not in acceptableExtensions:
		files.remove(name)


### Make shorter data dict ###
shortenStart = time.time()
DATA = {}

print("Loading/Shortening Image Data...")
for imageName in tqdm(files):
# for imageName in files:
	loopStart = time.time()
	temp_PATH = Directory_PATH + '/' + imageName
	IM = Image.open(temp_PATH)
	if sum(IM.size) > 3000:
		newSize = (int(IM.size[0] / 1), int(IM.size[1] / 1))
		IM = IM.resize(newSize)
	full = list(IM.getdata())
	DATA[imageName] = shorten(full, shortenFactor)
print(f"\nFinished making small data in: {time.time() - shortenStart}")
# print(DATA)


### COMPARE DATA ###
print(f"\nImages: {files}\n")
matches = []								#record of matches to avoid double check
lengths = [len(name) for name in files]		#length of file names for output format
acceptableTimeGap = 43200 					#12 hours in seconds
acceptablePercent = 20

for baseIndex, baseImage in enumerate(files):
	for testIndex, testImage in enumerate(files):
		if baseIndex != testIndex:
			if set([baseImage, testImage]) not in matches and abs(os.path.getctime(Directory_PATH + '/' + testImage) - os.path.getctime(Directory_PATH + '/' + baseImage)) < acceptableTimeGap:
				try:
					compareStart = time.time()
					# difference = return_percent(Directory_PATH + '/' + baseImage, Directory_PATH + '/' + testImage)
					difference = return_percent(DATA[baseImage], DATA[testImage])
					if difference < acceptablePercent:
						matches.append(set([baseImage, testImage]))
						print(f"{baseImage} {' ' * (max(lengths) - len(baseImage))} {testImage} {' ' * (max(lengths) - len(testImage))} | {difference}%  {round((time.time() - compareStart), 2)}  -  MATCH FOUND")
					else:
						print(f"{baseImage} {' ' * (max(lengths) - len(baseImage))} {testImage} {' ' * (max(lengths) - len(testImage))} | {difference}%  {round((time.time() - compareStart), 2)}")
				
				except AssertionError:
					# print(f"{baseImage} \t{testImage} \t | Incompatible Images")
					pass

	

print(f"\n{len(matches)} matches found.")
print(f"Finished in: {time.time() - FULLSTART}")