import numpy as np

filePATH = "/Users/ethanbolton/Desktop/COPY_DETECT/edjoLabsSolution/my_implementation/datafiles/1556507519.npy"

loaded = np.load(filePATH, allow_pickle=True)
DATA = loaded[()]

print(type(DATA))
for i in DATA:
	print(i)