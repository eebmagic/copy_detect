import os, time

# directory_PATH = input("Drag folder here: ").strip()
directory_PATH = "/Users/ethanbolton/Desktop/COPY_DETECT/imageSets/basicImages" #Fo testing purposes

files = os.listdir(directory_PATH)
acceptableExtensions = ['.png', '.PNG', '.jpg', '.JPG']
for name in files:
	if os.path.splitext(name)[1] not in acceptableExtensions:
		files.remove(name)

print(files)


from PIL import Image

def get_date_taken(path):
	return Image.open(path)._getexif()[36867]

# print(get_date_taken(directory_PATH + '/' + files[0]))

for name in files:
	print('\n', name)
	# print("Last modified: %s" % time.ctime(os.path.getmtime(directory_PATH + '/' + name)))
	print("Created: %s" % time.ctime(os.path.getctime(directory_PATH + '/' + name)))
	print("Created: %s" % (os.path.getctime(directory_PATH + '/' + name)))

