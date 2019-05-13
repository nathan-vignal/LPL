from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.util import bigrams


# sent = "There was Eru, the One, who in Arda is called lluvatar; and he made first the Ainur, the Holy Ones, that were the offspring of his thought, and they were with him before aught else was made. And he spoke to them, propounding to them themes of music; and they sang before him, and he was glad. But for a long while they sang only each alone, or but few together, while the rest hearkened; for each comprehended only that part of me mind of lluvatar from which he came, and in the understanding of their brethren they grew but slowly. Yet ever as they listened they came to deeper understanding, and increased in unison and harmony. "
first = ["hi","hi"]
first = " ".join(first)
second = "HI dogo"
cfdist = []
cfdist.append(FreqDist(word_tokenize(first)))
cfdist.append(FreqDist(word.lower() for word in word_tokenize(second)))
print(list((cfdist[0] + cfdist[1]).values()))
# cfdist.append(bigrams(sent))
#
#
# sum = {}
# for c in cfdist:
#     for item in c.items():
#         if item[0] in sum:
#             sum[item[0]] += item[1]
#         else:
#             sum[item[0]] = item[1]
#
# print(sum)
# FreqDist(word.lower() for word in word_tokenize(sent))
#
# cfdist[0].count()



# print(cfdist.items())
#
#
#
# for item in cfdist.items():
#     print(item[1])
