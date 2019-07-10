#From this page:
#	https://rosettacode.org/wiki/Percentage_difference_between_images#Python

'''
WARNING:
	This is the straight method for comparing images from the website.
	I've modified this to only check some of the pixel values for the sake of speed.
'''

from PIL import Image

# i1_PATH = input("Drag Image1 here: ").strip()
# i2_PATH = input("Drag Image1 here: ").strip()
i1_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages/bag.png"
i2_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages/tableA.png"


def return_percent(inputOne, inputTwo):
	i1 = Image.open(inputOne)
	i2 = Image.open(inputTwo)

	assert i1.mode == i2.mode, "Different kinds of images."
	assert i1.size == i2.size, "Different sizes."
	 
	pairs = zip(i1.getdata(), i2.getdata())
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	 
	ncomponents = i1.size[0] * i1.size[1] * 3
	percent = (dif / 255.0 * 100) / ncomponents
	return int(percent)

print(f"Difference: {return_percent(i1_PATH, i2_PATH)}%")