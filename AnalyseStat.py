import pandas as pd

def analyseCorpus(typeOfAnalysis, corpus):
    """
    :param typeOfAnalysis:  str
    :param corpus: array of Corpus
    :return:
    """
    if not isinstance(typeOfAnalysis, str):
        print("typeOfAnalysis must be a string")
        return -1
    if 'nombre d\'IPU' in typeOfAnalysis:
        data = pd.Series(corpus.getNbOfLinesByFile())
    elif 'nombre de mots' in typeOfAnalysis:
        data = pd.Series(corpus.getNumberOfWordsByFile())
    elif "temps par fichier" in typeOfAnalysis:
        data = pd.Series(corpus.getDurationByFile())
        data /= 60
    elif "mots/ipu" in typeOfAnalysis:
        data = pd.Series(corpus.getNumberOfWordsByFile())
        ipuParFichier = corpus.getNbOfLinesByFile()
        for i in range(0, len(data)):
            data[i] /= ipuParFichier[i]
    elif "secondes/ipu" in typeOfAnalysis:
        data = pd.Series(corpus.getDurationByFile())
        nbOfLines = corpus.getNbOfLinesByFile()
        for i in range(0, len(data)):
            data[i] /= nbOfLines[i]
    elif "mots/secondes" in typeOfAnalysis:
        data = corpus.getNumberOfWordsByFile()
        durationByFile = corpus.getDurationByFile()
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