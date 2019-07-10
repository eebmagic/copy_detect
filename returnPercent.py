from PIL import Image

file_PATH_one = input("\n\tDrag file ONE here: ").strip()
file_PATH_two = input("\n\tDrag file TWO here: ").strip()

one = Image.open(file_PATH_one)
two = Image.open(file_PATH_two)

data = [one.getdata(), two.getdata()]

def listSimilarities(list_one, list_two):
	count = 0
	for i in range(min([len(list_one), len(list_two)])):
		if list_one[i] == list_two[i]:
			count += 1

	return(float(count / len(list_one)) * 100)

print(f"The two pictures are {listSimilarities(data[0], data[1])}% in common")