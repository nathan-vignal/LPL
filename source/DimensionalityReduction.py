from __future__ import print_function
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from os import path
from sklearn.cluster import KMeans
from source.pathManagment import getTextPath, getPathToSerialized
import numpy as np
import pickle
import os
import math

pd.options.display.max_columns = 10


def analysisInManyDimensions(arrayOfCorpus):
    data = []

    # search for each corpus the infos we want
    for corpus in arrayOfCorpus:
        corpusData = []
        # variable
        corpusData.append(corpus.getMeanLexicalRichness(forEachFile=True))

        # variable
        nbWords = corpus.getNumberOfWords(forEachFile=True)
        nbFill = corpus.countSpecialWords(
            open(path.join(getTextPath(), "fill_" + corpus.getLanguage()), "r")
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
        formality = corpus.countSpecialWords(
            open(path.join(getTextPath(), "formality_" + corpus.getLanguage()), "r")
                                             .readlines()[0]
                                             .split(','), forEachFile=True
                                             )

        lowFormality = corpus.countSpecialWords(open(path.join(getTextPath(), "lowFormality_" + corpus.getLanguage()), "r")
                                                .readlines()[0]
                                                .split(','), forEachFile=True
                                                )

        temp = []
        for i in range(0, len(formality)):
            if formality[i] > 0:
                temp.append(lowFormality[i]/formality[i])
            else:
                temp.append(lowFormality[i])
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


def freqAnalysis(corpus, numberOfWords, printMostCommon=False):

    short = corpus.getShortIpuDistFreq()

    longStart, longEnd = corpus.getLongIpuDistFreq()

    mostCommonShort = [x[0] for x in short.most_common(numberOfWords)]
    mostCommonLongStart = [x[0] for x in longStart.most_common(numberOfWords)]
    mostCommonLongEnd = [x[0] for x in longEnd.most_common(numberOfWords)]

    # if printMostCommon:
    #     print("most common in short IPUs : " + str(mostCommonShort))
    #     print("most common as first word in Long IPU : " + str(mostCommonLongStart))
    #     print("most common as last word in Long IPU : " + str(mostCommonLongEnd))

    # storing the most common words inside a dictionary
    # We are also adding a postfix to the word because we don't want categories to mix
    mostCommonWords = {}
    for word in mostCommonShort:
        mostCommonWords[word+"_Short"] = corpus.getWordFreqShortIPU(word)

    for word in mostCommonLongStart:
        mostCommonWords[word+"_LStart"] = corpus.getWordFreqLongIpu(word, isStart=True)

    for word in mostCommonLongEnd:
        mostCommonWords[word+"_LEnd"] = corpus.getWordFreqLongIpu(word, isStart=False)

    dataFrame = pd.DataFrame(mostCommonWords)
    return dataFrame


def SWBDAnalysis(swbdCorpus, speakerData, labelWanted = None, numberOfWords=5, clusterKMean=0):
    """

    :param swbdCorpus:
    :param speakerData:
    :param labelWanted:
    :param numberOfWords:
    :param clusterKMean: if 0 we will use label
    :return:
    """
    dataframe = None

    if not os.path.isfile(path.join(getPathToSerialized(), "swbdDataframe")):

        frequencyAnalysis = freqAnalysis(swbdCorpus, numberOfWords=numberOfWords, printMostCommon=True)


        dimensionAnalysis = analysisInManyDimensions([swbdCorpus])
        dataframe = pd.concat([frequencyAnalysis, dimensionAnalysis], axis=1, sort=False)


        f = open(path.join(getPathToSerialized(), "swbdDataframe"), "wb")
        pickle.dump(dataframe, f)
        f.close()
    else:
        f = open(path.join(getPathToSerialized(), "swbdDataframe"), "rb")
        dataframe = pickle.load(f)
        f.close()

    # grouping files by speaker
    eachFilespeakerID = swbdCorpus.getSpeakerByFile()
    dataframe["idSpeaker"] = eachFilespeakerID
    dataframe = dataframe.groupby(['idSpeaker']).mean()



    if clusterKMean == 0 and labelWanted is not None:
        # we cluster by labelWanted
        filteredSpeaker = {}
        for speaker in speakerData:
            for info in speakerData[speaker]:
                if info == labelWanted:
                    filteredSpeaker[speaker] = speakerData[speaker][info]

        dataframe["label"] = pd.Series(filteredSpeaker)
        #dataframe.index = pd.RangeIndex(len(dataframe.index)) does not work
        dataframe.index = np.arange(len(dataframe))

    elif clusterKMean > 0:

        dataframe.index = pd.RangeIndex(len(dataframe.index))  # restarting the indexes is important
        # because the current indices are speakers's identification number

        kmeanModel = KMeans(n_clusters=clusterKMean).fit(dataframe)
        clusters = kmeanModel.predict(dataframe)  # associate a cluster to each speaker
        dataframe["label"] = pd.Series(dict(enumerate(clusters)))  # going from a list to a dict and assigning
    else:
        print("need either label wanted or clusterKMean in function SWBDAnalysisSpeakers")

    f = open(path.join(getPathToSerialized(), "swbdDataframeBySpeaker"), "wb")
    pickle.dump(dataframe, f)
    f.close()

    return dataframe, eachFilespeakerID


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
    finalDf = finalDf[np.invert(finalDf['principal component 2'].isna())]  # when we delete extreme values we delete
    # rows that are still in dataFrame, so we obtain NaN when we merge dataframe and principalDf, here we delete the Nan
    return finalDf, pca


def displayPlot(dataFrame, groupByLabel=False):
    dotSize = 5
    if groupByLabel:
        dataFrame = dataFrame.groupby(["label"]).mean()
        dataFrame = dataFrame.reset_index()
        dotSize *= 10
    print(dataFrame)



    f = open(path.join(getPathToSerialized(), "mtplotToBokeh"), "wb")
    pickle.dump(dataFrame, f)
    f.close()

    fig = plt.figure(figsize=(8, 8))
    # creating the axes
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)
    # getting the labels inside the dataframe
    labels = dataFrame['label'].unique()

    colors = ['red', 'green', 'blue', 'brown', 'black']
    # if there's more labels than colors fill the rest with black
    colors.extend(['black'] * (len(labels)-len(colors)))

    # for each label display all the conversations associated
    for target, color in zip(labels, colors):
        indicesToKeep = dataFrame['label'] == target
        ax.scatter(dataFrame.loc[indicesToKeep, 'principal component 1']
                   , dataFrame.loc[indicesToKeep, 'principal component 2']
                   , c=color
                   , s=dotSize)
    ax.legend(labels)
    ax.grid()

    plt.show()


