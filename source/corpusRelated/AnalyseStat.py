import pandas as pd
import numpy as np

def analyseCorpus(typeOfAnalysis, corpus):
    """
    process a statistic analysis on the given corpus given the typeOfAnalysis (eg: nombre de mots)
    :param typeOfAnalysis:  str
    :param corpus: Corpus instance
    :return:
    """
    if not isinstance(typeOfAnalysis, str):
        print("typeOfAnalysis must be a string")
        return -1
    if 'nombre d\'IPU' in typeOfAnalysis:
        data = pd.Series(corpus.getNbOfLines())
    elif 'nombre de mots' in typeOfAnalysis:
        data = pd.Series(corpus.getNumberOfWords())
    elif "temps" in typeOfAnalysis:
        data = pd.Series(corpus.getDuration())
        data /= 60
    elif "mots/ipu" in typeOfAnalysis:
        data = pd.Series(corpus.getNumberOfWords())
        ipuParFichier = corpus.getNbOfLines()
        for i in range(0, len(data)):
            data[i] /= ipuParFichier[i]
    elif "secondes/ipu" in typeOfAnalysis:
        data = pd.Series(corpus.getDuration())
        nbOfLines = corpus.getNbOfLines()
        for i in range(0, len(data)):
            data[i] /= nbOfLines[i]
    elif "mots/secondes" in typeOfAnalysis:
        data = corpus.getNumberOfWords()
        durationByFile = corpus.getDuration()
        for i in range(0, len(data)):
            if durationByFile[i] == 0:
                data[i] = 0
                continue
            data[i] = data[i] / durationByFile[i]
        data = pd.Series(data)
    elif"nombre de fichier" in typeOfAnalysis:
        data = [1] * corpus.getNbOfFiles() # senf back the number of file in each file stupid but it helps abstraction
    else:
        print("invalid analyze function ")
        data = []  # prevent crash
    return data


def createDataSpeakerAnalysis(corpus, speakersId, analyseFunction, discriminationCritirion):
    """

    :param corpus: instance of Corpus
    :param speakersId: {'1268': {'age': '29', 'geography': 'SOUTH MIDLAND', 'level_study': '2', 'sex': 'FEMALE'},'1269'...
    :param analyseFunction: str (eg: nombre de mots
    :param discriminationCritirion: str (eg: sex)
    :return:
    """
    eachFilespeakerID = corpus.getSpeakerByFile()

    eachCorpusSpeakers = []
    for speakerId in eachFilespeakerID:
        eachCorpusSpeakers.append(speakersId[speakerId])

    data = analyseCorpus(analyseFunction, corpus)

    for speaker in eachCorpusSpeakers:
        if discriminationCritirion not in speaker:
            print("unrecognized speaker discrimination" + str(discriminationCritirion))
            return -1

    dataBySpeakerType = {}
    for speakerNb in range(0, len(data)):
        speakerType = eachCorpusSpeakers[speakerNb][discriminationCritirion]  # eg: male or female
        if speakerType in dataBySpeakerType:
            dataBySpeakerType[speakerType] += data[speakerNb]
        else:
            dataBySpeakerType[speakerType] = data[speakerNb]


    xData = []
    xAxis = []
    y = []
    # if there's too many x axis value and we can group can group them, we group values together
    # eg 1 2 3 4 -> 1_2 3_4
    isDigitType = True
    for key in dataBySpeakerType.keys():
        if not key.isdigit():
            isDigitType = False
            break

    if isDigitType and len(dataBySpeakerType.keys()) > 10:
        for key in dataBySpeakerType.keys():
            xData.append(key)
            y = [dataBySpeakerType.keys()[key]]
        # if there is too many categories we create groups
        xAxis.append(np.sort(np.asarray(xData)))
            # np.split(xAxis, 10)

    else:
        xData = [k for k in dataBySpeakerType.keys()]

        y = []
        for key in dataBySpeakerType:
            y.append(dataBySpeakerType[key])
        # sorting the bars means sorting the range factors
        xAxis = sorted(xData, key=lambda x: y[xData.index(x)])  # xAxis contains the values that will serve
        # as the x axis values eg (male, Female)
    return xData, y, xAxis