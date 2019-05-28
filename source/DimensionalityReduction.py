from __future__ import print_function
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from os import path
from source.pathManagment import getTextPath, getPathToSerialized
import pickle

pd.options.display.max_columns = 10


def analysisInManyDimensions(arrayOfCorpus):
    data = []
    #arrayOfCorpus = [arrayOfCorpus[0],arrayOfCorpus[1]] subarray used for test only

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


def freqAnalysis(corpus):

    short = corpus.getShortIpuDistFreq()

    longStart, longEnd = corpus.getLongIpuDistFreq()

    mostCommonShort = [x[0] for x in short.most_common(5)]
    print(mostCommonShort)
    mostCommonLongStart = [x[0] for x in longStart.most_common(5)]
    print(mostCommonLongStart)
    mostCommonLongEnd = [x[0] for x in longEnd.most_common(5)]
    print(mostCommonLongEnd)

    # storing the most common words inside a dictionnary
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


def SWBDAnalysisSpeakers(swbdCorpus, speakerData, labelWanted, isFreqAnalysis =False):

    if isFreqAnalysis:
        dataframe = freqAnalysis(swbdCorpus)
    else:
        dataframe = analysisInManyDimensions([swbdCorpus])

    f = open(path.join(getPathToSerialized(), "swbdDataframe"), "wb")
    pickle.dump(dataframe, f)
    f.close()

    # f = open(path.join(getPathToSerialized(), "swbdDataframe"), "rb")
    # dataframe = pickle.load(f)
    # f.close()

    eachFilespeakerID = swbdCorpus.getSpeakerByFile()
    dataframe["idSpeaker"] = eachFilespeakerID

    # filtering the info in speakerData and keeping only labelWanted
    # speakerDAta look like {'1000': {'sex': 'FEMALE', 'age': '36', 'geography': 'SOUTH MIDLAND', 'level_study': '1'}..
    # filteredSpeaker will look like {'1000': '1', '1001': '3',...} if labelWanted is level_study
    filteredSpeaker = {}
    for speaker in speakerData:
        for info in speakerData[speaker]:
            if info == labelWanted:
                filteredSpeaker[speaker] = speakerData[speaker][info]

    dataframe = dataframe.groupby(['idSpeaker']).mean()
    dataframe["label"] = pd.Series(filteredSpeaker)
    dataframe.index = pd.RangeIndex(len(dataframe.index))

    return dataframe


def pca(dataFrame):
    print(dataFrame.columns)
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


def displayPlot(dataFrame, groupByLabel=False):
    dotSize = 5
    if groupByLabel:
        dataFrame = dataFrame.groupby(["label"]).mean()
        dataFrame = dataFrame.reset_index()
        dotSize *= 10
    print(dataFrame.columns)





    fig = plt.figure(figsize=(8, 8))
    #creating the axes
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)
    #getting the labels inside the dataframe
    labels = dataFrame['label'].unique()

    colors = ['red', 'green', 'blue', 'brown', 'black']
    # if there's more labels than colors fill the rest with black
    colors.extend(['black'] * (  len( dataFrame.groupby(['label']) )-len(colors)  ))

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


