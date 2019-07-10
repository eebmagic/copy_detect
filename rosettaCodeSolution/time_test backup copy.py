from PIL import Image
import os
import time
start = time.time()


def shorten(fullData, factor):
	shortOutput = []
	indexes = [i*factor for i in range(int(len(fullData)/factor))]
	for ind in indexes:
		shortOutput.append(fullData[ind])



def return_percent(inputOne, inputTwo):
	funcStart = time.time()

	i1 = Image.open(inputOne)
	i2 = Image.open(inputTwo)
	print(f"\nOpen images: {time.time() - funcStart}")


	assert i1.mode == i2.mode, "Different kinds of images."
	assert i1.size == i2.size, "Different sizes."
	
	data1 = i1.getdata()
	data2 = i2.getdata()
	newData1 = []
	newData2 = []
	print(f"Got data: {time.time() - funcStart}")

	shortenFactor = 50
	indexes = [i*shortenFactor for i in range(int(len(data1)/shortenFactor))]
	for ind in indexes:
		newData1.append(data1[ind])
		newData2.append(data2[ind])
	print(f"Made new short data: {time.time() - funcStart}")


	pairs = zip(newData1, newData2)
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	print(f"Made comparison: {time.time() - funcStart}")

	ncomponents = (i1.size[0] * i1.size[1] * 3) / shortenFactor
	percent = (dif / 255.0 * 100) / ncomponents
	print(f"Made calcs: {time.time() - funcStart}")
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
DATA = {}
for imageName in files:
	DATA[imageName] = shorten(Directory_PATH + '/' + imageName)


print(f"\nImages: {files}\n")
matches = []								#record of matches to avoid double check
lengths = [len(name) for name in files]		#length of file names for output format
acceptableTimeGap = 43200 					#12 hours in seconds

for baseIndex, baseImage in enumerate(files):
	for testIndex, testImage in enumerate(files):
		if baseIndex != testIndex:
			if set([baseImage, testImage]) not in matches and abs(os.path.getctime(Directory_PATH + '/' + testImage) - os.path.getctime(Directory_PATH + '/' + baseImage)) < acceptableTimeGap:
				try:
					compareStart = time.time()
					difference = return_percent(Directory_PATH + '/' + baseImage, Directory_PATH + '/' + testImage)
					if difference < 20:
						matches.append(set([baseImage, testImage]))
						print(f"{baseImage} {' ' * (max(lengths) - len(baseImage))} {testImage} {' ' * (max(lengths) - len(testImage))} | {difference}%  {round((time.time() - compareStart), 2)}  -  MATCH FOUND")
					else:
						print(f"{baseImage} {' ' * (max(lengths) - len(baseImage))} {testImage} {' ' * (max(lengths) - len(testImage))} | {difference}%  {round((time.time() - compareStart), 2)}")
				
				except AssertionError:
					# print(f"{baseImage} \t{testImage} \t | Incompatible Images")
					pass

				


print(f"Finished in: {time.time() - start}")