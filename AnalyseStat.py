class AnalyseStat:
    @staticmethod
    def analyseCorpus(typeOfAnalysis, corpus):
        """

        :param typeOfAnalysis:  str
        :param corpus: array of Corpus
        :return:
        """
        if not isinstance(corpus, list):
            corpus = [corpus]
        if not isinstance(typeOfAnalysis, str):
            print("typeOfAnalysis must be a string")
            return -1