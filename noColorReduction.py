
from PIL import Image
import os

################
### SETTINGS ###
resolution_percent = 0.10
simlarity_threshold = 20
################

# Directory_PATH = input("\n\tDrag directory here: ").strip()
Directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/noScreenshots/OUTPUTS"
if Directory_PATH[:-1] == '/':
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

def saveImage(inputName, SIZE, inputData):
	newIm = Image.new("RGB", SIZE)
	newIm.putdata(inputData)
	newIm.save(inputName + "_output.png")

def listSimilarities(list_one, list_two):
	count = 0
	#identical pixels in image
	for i in range(len(list_one)):
		if list_one[i] == list_two[i]:
			count += 1
	return(float(count / len(list_one)) * 100)

def colorCountCompare(list_one, list_two):
	global simlarity_threshold

	### COUNT FOR ONE ###
	tracking_dictionary_one = {}
	for point in list_one:
		if point in tracking_dictionary_one:
			tracking_dictionary_one[point] += 1
		else:
			tracking_dictionary_one[point] = 1

	### COUNT FOR TWO ###
	tracking_dictionary_two = {}
	for point in list_two:
		if point in tracking_dictionary_two:
			tracking_dictionary_two[point] += 1
		else:
			tracking_dictionary_two[point] = 1


	### ADD ZERO POINTS FOR ONE ###
	for point in tracking_dictionary_one:
		if point not in tracking_dictionary_two:
			tracking_dictionary_two[point] = 0
	
	### ADD ZERO POINTS FOR TWO ###
	for point in tracking_dictionary_two:
		if point not in tracking_dictionary_one:
			tracking_dictionary_one[point] = 0

	## GET TOTALS ##
	one_total = 0
	two_total = 0
	for point in tracking_dictionary_one:
		one_total += tracking_dictionary_one[point]
		two_total += tracking_dictionary_two[point]

	counts = []
	for point in tracking_dictionary_one:
		counts.append(tracking_dictionary_one[point])
	### CALCULATE DIFFERENCES ###
	count = 0
	for point in tracking_dictionary_one:
		diff = abs(tracking_dictionary_one[point] - tracking_dictionary_two[point])
		if diff < simlarity_threshold:
			count += 1
	return(round((count/len(tracking_dictionary_one) * 100), 2))

####################################################################
####################################################################
####################################################################

allData = []
print("Loading image RGB data...")
for filename in os.listdir(Directory_PATH):
	if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
		file_PATH = Directory_PATH + '/' + filename
		im = Image.open(file_PATH)
		im = lowerSize(im, resolution_percent)
		RGB_Data = decreaseColors(im, 180)
		# RGB_Data = im.getdata()

		allData.append({"filename":filename, "imageData":RGB_Data, 'imageSize':im.size})

for baseIndex, baseIMAGE in enumerate(allData):
	for testIndex, testIMAGE in enumerate(allData):
		if baseIndex != testIndex:
			comparison = colorCountCompare(baseIMAGE['imageData'], testIMAGE['imageData'])
			print(f"{baseIMAGE['filename']} with {testIMAGE['filename']} gives \t{comparison}%")
			if comparison >= 99.9:
				print("\t\tMATCH FOUND")


