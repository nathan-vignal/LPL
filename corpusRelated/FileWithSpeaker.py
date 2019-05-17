from corpusRelated.File import File
import copy


class FileWithSpeaker(File):

    def __init__(self, path, speaker, corpus):
        File.__init__(self, path, corpus)
        self.__speaker = speaker

    def getSpeaker(self):
        return copy.copy(self.__speaker)

