from PIL import Image
import os
import time
start = time.time()


def return_percent(inputOne, inputTwo):
	i1 = Image.open(inputOne)
	i2 = Image.open(inputTwo)

	assert i1.mode == i2.mode, "Different kinds of images."
	assert i1.size == i2.size, "Different sizes."
	
	data1 = i1.getdata()
	data2 = i2.getdata()
	newData1 = []
	newData2 = []

	shortenFactor = 50
	indexes = [i*shortenFactor for i in range(int(len(data1)/shortenFactor))]
	for ind in indexes:
		newData1.append(data1[ind])
		newData2.append(data2[ind])


	pairs = zip(newData1, newData2)
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	 
	ncomponents = (i1.size[0] * i1.size[1] * 3) / shortenFactor
	percent = (dif / 255.0 * 100) / ncomponents
	return int(percent)


########################################################################
##### MAIN #####

# Directory_PATH = input("Drag folder here: ").strip()
Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages" #For testing purposes
# Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/testImages" #For testing purposes

files = os.listdir(Directory_PATH)
acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']
for name in files:
	if os.path.splitext(name)[1] not in acceptableExtensions:
		files.remove(name)

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
					difference = return_percent(Directory_PATH + '/' + baseImage, Directory_PATH + '/' + testImage)
					if difference < acceptablePercent:
						matches.append(set([baseImage, testImage]))
						print(f"{baseImage} {' ' * (max(lengths) - len(baseImage))} {testImage} {' ' * (max(lengths) - len(testImage))} | {difference}%  {round((time.time() - compareStart), 2)}  -  MATCH FOUND")
					else:
						print(f"{baseImage} {' ' * (max(lengths) - len(baseImage))} {testImage} {' ' * (max(lengths) - len(testImage))} | {difference}%  {round((time.time() - compareStart), 2)}")
				
				except AssertionError:
					# print(f"{baseImage} \t{testImage} \t | Incompatible Images")
					pass

				

print(f"\n{len(matches)} matches found.")
print(f"Finished in: {time.time() - start}")