from PIL import Image
import os

def lowerSize(inputImageObject, percentRate):
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