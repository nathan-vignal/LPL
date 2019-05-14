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



data = []
for corpus in arrayOfCorpus:
    corpusData = []

    # variable
    corpusData.append(corpus.getMeanLexicalRichness(forEachFile=True))

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
    corpusData.append(corpus.getRatioSpecialIpu("feedback_"+corpus.getLanguage()))

    # variable
    corpusData.append(corpus.getSpecialIpuMeanSize("not feedback_"+corpus.getLanguage()))

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
    data.append(corpusData)

print(data)

#  end catching data
