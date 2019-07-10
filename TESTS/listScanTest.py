sampleLists = [[(180, 180, 180), (180, 180, 180), (180, 180, 180), (180, 180, 0), (180, 180, 180), (180, 180, 180)], [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], [(180, 0, 0), (180, 0, 0), (180, 0, 0), (0, 0, 0), (0, 0, 0)]]

def similarities(list_one, list_two):
	count = 0
	for i in range(len(list_one)):
		if list_one[i] == list_two[i]:
			count += 1
	percentMatch = float(count / len(list_one)) * 100
	return percentMatch

allData = []
for LIST in sampleLists:
	allData.append({"imageData":LIST, "length":len(LIST)})

for index, baseImage in enumerate(allData):
	for i, image in enumerate(allData):
		if index != i and baseImage['length'] == image['length']:
			print(f"Base: {index} | testImage: {i} | match: {similarities(baseImage['imageData'], image['imageData'])}%")

	