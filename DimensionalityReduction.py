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


def analysisInManyDimensions(arrayOfCorpus):
    data = []
    #arrayOfCorpus = [arrayOfCorpus[0],arrayOfCorpus[1]] subarray used for test only

    # search for each corpus the infos we want
    for corpus in arrayOfCorpus:
        corpusData = []
        # variable
        corpusData.append(corpus.getMeanLexicalRichness(forEachFile=True),)

        # variable
        nbWords = corpus.getNumberOfWords(forEachFile=True)
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
    #  changing format to create a pandas dataFrame
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
    return dataFrame


def pca(dataFrame):

    features = list(dataFrame.columns)
    features.remove('label')
    # Separating out the features
    x = dataFrame.loc[:, features].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)

    principalDf = pd.DataFrame(data = principalComponents
                 , columns=['principal component 1', 'principal component 2'])
    principalDf = principalDf[principalDf['principal component 1'] < 4]
    principalDf = principalDf[principalDf['principal component 2'] < 4]

    finalDf = pd.concat([principalDf, dataFrame[['label']]], axis=1)

    return finalDf, pca


def displayPlot(dataFrame):

    fig = plt.figure(figsize=(8, 8))
    #creating the axes
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)
    #getting the labels inside the dataframe
    labels = dataFrame['label'].unique()

    colors = ['red', 'green', 'blue', 'pink', 'yellow']
    # if there's more labels than colors fill the rest with black
    colors.extend(['black'] * (  len( dataFrame.groupby(['label']) )-len(colors)  ))

    # for each label display all the conversations associated
    for target, color in zip(labels, colors):
        indicesToKeep = dataFrame['label'] == target
        ax.scatter(dataFrame.loc[indicesToKeep, 'principal component 1']
                   , dataFrame.loc[indicesToKeep, 'principal component 2']
                   , c=color
                   , s=5)
    ax.legend(labels)
    ax.grid()

    plt.show()


