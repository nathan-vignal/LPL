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


for