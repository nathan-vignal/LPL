import pickle
from source.Cell import Cell

# cell = Cell()
# print(cell)
# f = open("./tests/pickling", "wb")
#
# pickle.dump(cell, f)
#
# f.close()

f = open("./tests/pickling", "rb")


array = pickle.load(f)

print(array)

f.close()