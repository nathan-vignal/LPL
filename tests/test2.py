import pickle
from os import path
from source.pathManagment import getPathToSerialized
from source.Cell import Cell

# cell = Cell()
# print(cell)
# f = open("./tests/pickling", "wb")
#
# pickle.dump(cell, f)
#
# f.close()

f = open(path.join(getPathToSerialized(), "arrayOfCorpus"), "rb")


array = pickle.load(f)
f.close()



