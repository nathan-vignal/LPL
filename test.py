from __future__ import print_function
from bokeh.plotting import figure
import numpy as np
from bokeh.io import output_notebook
from os import listdir
from corpusRelated.CorpusReader import createCorpusFromDirectory
from corpusRelated.Speakers import getSpeakers
import RadarGraph
from bokeh.models.renderers import GlyphRenderer
from bokeh.io import show, push_notebook
import RadarModel
import warnings
from Graph import Graph
import Cell
import Model
import Input
from bokeh.io import show
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


metaDataToLoad = ["sex", "age", "geography", "level_study"]
metaDataFiles = {"SWBD": "./data/metadata/"}
conversationInfo = {}
speakers = {}
for metadata in metaDataFiles:
    tempConversationInfo, tempspeakers = getSpeakers(metaDataFiles[metadata], metaDataToLoad)
    conversationInfo[metadata] = tempConversationInfo
    speakers[metadata] = tempspeakers


def initCorpus():
    global conversationInfo
    arrayOfCorpus = []
    sourceDirectory = "./data/corpus/"
    # search source directory for corpus and fill corpus object with files inside array corpuses
    for directoryName in listdir(sourceDirectory):
        newCorpus = createCorpusFromDirectory(directoryName, sourceDirectory + '/' + directoryName, conversationInfo)

        arrayOfCorpus.append(newCorpus)
    return arrayOfCorpus

# --------------------------------------------------------------------------------------------------------


arrayOfCorpus = initCorpus()


# ---------------------------------------------------------

data = []
arrayOfCorpus = [arrayOfCorpus[0]]  # subarray used for test only

for corpus in arrayOfCorpus:
    corpusData = []
    # variable
    corpusData.append(corpus.getMeanLexicalRichness(forEachFile=True),)

    # variable
    nbWords = corpus.getMeanNumberOfWords(forEachFile=True)
    nbFill = corpus.countSpecialWords(
        open("./corpusRelated/txt/fill_"+corpus.getLanguage(), "r")
            .readlines()[0]
            .split(',')
        , forEachFile=True
    )

    temp = []
    for i in range(0, len(nbFill)):
        if nbWords[i] > 0:
            temp.append(nbFill[i]/nbWords[i])
        else:
            temp.append(0)
    corpusData.append(temp)

    # variable
    corpusData.append(corpus.getRatioSpecialIpu("feedback_"+corpus.getLanguage(), forEachFile=True))

    # variable
    corpusData.append(corpus.getSpecialIpuMeanSize("not feedback_"+corpus.getLanguage(), forEachFile=True))

    # variable

    formality = corpus.countSpecialWords(open("./corpusRelated/txt/formality_"+corpus.getLanguage(), "r")
                                         .readlines()[0]
                                         .split(','), forEachFile=True
                                         )

    lowFormality = corpus.countSpecialWords(open("./corpusRelated/txt/lowFormality_"+corpus.getLanguage(), "r")
                                            .readlines()[0]
                                            .split(','), forEachFile=True
                                            )

    temp = []
    for i in range(0, len(formality)):
        if formality[i] > 0:
            temp.append(lowFormality[i]/formality[i])
        else:
            temp.append(0)
    corpusData.append(temp)

    # label
    corpusName = corpus.getName()
    corpusData.append([corpusName] * corpus.getNbOfFiles())
    ####
    data.append(corpusData)



tempData = []
for i in range(0, len(data[0])):
    temp = []

    for corpusData in data:
        temp.extend(corpusData[i])
    tempData.append(pd.Series(temp))

data = tempData

dataFrame = pd.DataFrame({'lexical richness': data[0]
                             , 'ratio fill': data[1]
                             , 'ratio ipu feedback': data[2]
                             , 'mean size not feedback IPU': data[3]
                             , 'formality ratio': data[4]
                             , 'label': data[5]})

print(dataFrame)

# starting processing
features = ['lexical richness'
    , 'ratio fill'
    , 'ratio ipu feedback'
    , 'mean size not feedback IPU'
    , 'formality ratio']
# Separating out the features
x = dataFrame.loc[:, features].values
print(x)
# Separating out the target
y = dataFrame.loc[:,['label']].values
# Standardizing the features
x = StandardScaler().fit_transform(x)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns=['principal component 1', 'principal component 2'])
principalDf = principalDf[principalDf['principal component 1'] < 4]
principalDf = principalDf[principalDf['principal component 2'] < 4]

finalDf = pd.concat([principalDf, dataFrame[['label']]], axis = 1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

labels = []
for corpus in arrayOfCorpus:
    labels.append(corpus.getName())

colors = ['red', 'green', 'blue', 'pink', 'black']
for target, color in zip(labels,colors):
    indicesToKeep = finalDf['label'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 5)
ax.legend(labels)
ax.grid()

plt.show()


