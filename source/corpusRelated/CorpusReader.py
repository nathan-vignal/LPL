from source.corpusRelated import FileWithSpeaker, Corpus
from source.corpusRelated import File, Fisher
from os import listdir


def createCorpusFromDirectory(type, path, convMap):

    newCorpus = Corpus.Corpus(type, path, type)

    files = []

    # case the corpus is fisher
    if type == "Fisher":
        savePath = path
        for fisherHalf in listdir(path):
            if fisherHalf == ".DS_Store":
                continue

            path = savePath + "/"+fisherHalf +"/data/bbn_orig/"
            for directory in listdir(path):
                if len(listdir(path + directory)) != 0 and directory != ".DS_Store":
                    if "auto-segmented" in listdir(path + directory):
                        for file in listdir(path + directory + "/auto-segmented"):
                            if ".trn" in file:  # we just want one object by conversation
                                speakerFile = Fisher.Fisher(path + directory + "/auto-segmented/", file[:-4]).getSons()
                                files.append(speakerFile[0])
                                files.append(speakerFile[1])
            newCorpus.addElements(files)

        return newCorpus

    # case the corpus is switchboard
    if type == 'SWBD':
        for filename in listdir(path):

            if len(filename) != 3 or filename == ".DS_Store":
                continue  # filtrage des fichiers inutiles
            for swbdDirectory in listdir(path + '/' + filename):
                if swbdDirectory == ".DS_Store":
                    continue
                for file in listdir(path + '/' + filename + '/' + swbdDirectory):
                    if "trans" in file:
                        if type in convMap:
                            if "A" in file:
                                isSpeakerB = 0
                            elif "B" in file:
                                isSpeakerB = 1
                            speakerId = convMap[type][swbdDirectory.replace("R", "")][isSpeakerB]
                            currentFile = FileWithSpeaker.FileWithSpeaker(
                                path+ '/' + filename
                                + '/' + swbdDirectory + '/' + file
                                , speakerId
                                , newCorpus)
                            files.append(currentFile)
        newCorpus.addElements(files)
        return newCorpus

    # case the corpus is something else with all files directly in the directory
    constructor = None
    if not newCorpus.getHasSpeaker():
        constructor = File.File
    else :
        constructor = FileWithSpeaker.FileWithSpeaker

    for filename in listdir(path):
        if filename == ".DS_Store":
            continue
        # the directory for switchboard has a specific architecture

        currentFile = constructor(path + "/" + filename, newCorpus)
        files.append(currentFile)



    newCorpus.addElements(files)
    return newCorpus
