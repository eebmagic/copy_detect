from PIL import Image
from ast import literal_eval

### GET FILE PATH ###
PATH = input("\n\tDrag image file here: ").strip()
print("\n")

### GET RGB DATA ###
im = Image.open(PATH)
originalData = list(im.getdata())


### MANIPULATE DATA ###
colorTolerance = int(input("What number would you like to use for the color resolution tolerance?(0-255): "))
lowerData = []
for point in originalData:
	newSet = []
	for num in point:
		newSet.append(num - (num % colorTolerance))
	newTuple = (newSet[0], newSet[1], newSet[2])
	lowerData.append(newTuple)


### MAKE IMAGE ###
newIm = Image.new("RGB", im.size)
newIm.putdata(lowerData)
newIm.save("GENERATED.png")

from os import system
system("open GENERATED.png")