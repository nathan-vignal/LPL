import Fisher
import Corpus
from os import listdir
import File
import FileWithSpeaker
def createCorpusFromDirectory(type, path, convMap):
    #path = sourceDirectory + directoryName
    newCorpus = Corpus.Corpus(type, path, type)

    files = []
    if type == "Fisher":
        path = path + "/Fisher1/data/bbn_orig/"
        for directory in listdir(path):
            if len(listdir(path + directory)) != 0:
                for file in listdir(path + directory + "/auto-segmented"):
                    if ".trn" in file:  # we just want one object by conversation
                        files.append(Fisher.Fisher(path + directory + "/auto-segmented/", file[:-4]))
        newCorpus.addElements(files)
        return newCorpus

    if type == 'SWBD':
        for filename in listdir(path):

            if len(filename) != 3:
                continue  # filtrage des fichiers inutiles
            for swbdDirectory in listdir(path + '/' + filename):

                for file in listdir(path + '/' + filename + '/' + swbdDirectory):
                    if "trans" in file:

                        if "A" in file:
                            isSpeakerB = 0
                        elif "B" in file:
                            isSpeakerB = 1
                        speakerId = convMap[swbdDirectory.replace("R", "")][isSpeakerB]
                        currentFile = FileWithSpeaker.FileWithSpeaker(
                            path+ '/' + filename
                            + '/' + swbdDirectory + '/' + file
                            , newCorpus.delimiter
                            , speakerId)
                        files.append(currentFile)
        newCorpus.addElements(files)
        return newCorpus

    for filename in listdir(path):
        # the directory for switchboard has a specific architecture

        currentFile = File.File(path + "/" + filename, newCorpus.delimiter)
        files.append(currentFile)

    newCorpus.addElements(files)
    return newCorpus
