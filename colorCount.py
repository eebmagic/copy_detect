##################################################
#	
#	This scans through images in a directory and finds near duplicates by lower resolution and color resolution
#
##################################################

from PIL import Image
import os

################
### SETTINGS ###
resolution_percent = 0.10
color_rate = 180
simlarity_threshold = 80
################


#Get Path
Directory_PATH = input("\n\tDrag directory here: ").strip()
if Directory_PATH[:-1] == "/":
	Directory_PATH = Directory_PATH[:-1]
print("")


def lowerSize(inputImage, rate):
	return inputImage.resize((round(im.size[0]*rate), round(im.size[1]*rate)), Image.ANTIALIAS)

def decreaseColors(inputImage, rate):
	data = list(inputImage.getdata())
	output = []
	for point in data:
		newSet = []
		for num in point[:3]:
			newSet.append(num - (num % rate))
		newTuple = (newSet[0], newSet[1], newSet[2])
		output.append(newTuple)
	return output

def listSimilarities(list_one, list_two):
	count = 0
	for i in range(len(list_one)):
		if list_one[i] == list_two[i]:
			count += 1
	return(float(count / len(list_one)) * 100)

def colorSimilarityCount(list_one, list_two):
	combos = {}
	#for 

def saveImage(inputName, SIZE, inputData):
	newIm = Image.new("RGB", SIZE)
	newIm.putdata(inputData)
	newIm.save(inputName + "_output.png")

##################################################################
### COLLECT IMAGE DATA ###
#Iterate through each file
allData = []
for filename in os.listdir(Directory_PATH):
	if filename.endswith(".png") or filename.endswith(".PNG") or filename.endswith(".jpg") or filename.endswith(".JPG"):
		file_PATH = Directory_PATH + '/' +filename
		im = Image.open(file_PATH)
		im = lowerSize(im, resolution_percent)
		RGB_Data = decreaseColors(im, color_rate)

		allData.append({"filename":filename, "imageData":RGB_Data, "dataLen":len(RGB_Data), "filePath":file_PATH, "imageObject":im, "imageSize":im.size})
		# saveImage(filename, im.size, RGB_Data)

### DISPLAY DATA ###
# for image in allData:
# 	print(f"{image['filename']} --> {image['dataLen']} --> {image['imageData'][:5]}")


### CHECK FOR SIMILAR ###
for baseIndex, baseIMAGE in enumerate(allData):
	for testIndex, testIMAGE in enumerate(allData):
		if baseIndex != testIndex and baseIMAGE['dataLen'] == testIMAGE['dataLen']:

			#Check similarities
			common = round(listSimilarities(baseIMAGE['imageData'], testIMAGE['imageData']), 2)
			print(f"{common}% match comparing {baseIMAGE['filename']} to {testIMAGE['filename']}.")
			if common > simlarity_threshold:
				print(f"{baseIMAGE['filename']} AND {testIMAGE['filename']} are {common}% Similar")

				saveImage(baseIMAGE['filename'], baseIMAGE['imageSize'], baseIMAGE['imageData'])
				saveImage(testIMAGE['filename'], testIMAGE['imageSize'], testIMAGE['imageData'])

