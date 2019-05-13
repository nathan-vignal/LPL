def isFeedBackIpu_en(ipuContent):
    return isSpecialIpu(ipuContent, 0.5, "./corpusRelated/txt/feedback_en", "./corpusRelated/txt/neutral_en", 3)

def isFeedBackIpu_fr(ipuContent):
    return isSpecialIpu(ipuContent, 0.5, "./corpusRelated/txt/feedback_fr", "./corpusRelated/txt/neutral_fr", 3)

def isFill(ipuContent):
    return isSpecialIpu(ipuContent, 1, "./corpusRelated/txt/fill_fr")

def isntFeedBackIpu_en(ipuContent):
    return not isSpecialIpu(ipuContent, 0.5, "./corpusRelated/txt/feedback_en", "./corpusRelated/txt/neutral_en", 3)

def isntFeedBackIpu_fr(ipuContent):
    return not isSpecialIpu(ipuContent, 0.5, "./corpusRelated/txt/feedback_fr", "./corpusRelated/txt/neutral_fr", 3)



def stringToIpuFct(ipuType):
    if "fill" in ipuType:
        return isFill
    elif "feedback_fr" == ipuType:
        return isFeedBackIpu_fr
    elif "feedback_en" == ipuType:
        return isFeedBackIpu_en
    elif "not feedback_fr" == ipuType:
        return isntFeedBackIpu_fr
    elif "not feedback_en" == ipuType:
        return isntFeedBackIpu_en
    return None



def isSpecialIpu(ipuContent, minRatio, fileWithKeyWords, fileWithNeutralKeywords = None, maxSize=9999):
    """
    :param ipuContent: [string]
    :param minRatio:
    :param fileWithKeyWords:
    :param MinSize:
    :return:
    """

    f1 = open(fileWithKeyWords, "r")
    specialWords = f1.readlines()[0].split(',')
    if fileWithNeutralKeywords is not None:
        f1 = open(fileWithNeutralKeywords, "r")
        neutralWords = f1.readlines()[0].split(',')

    nbSpecialWords = 0
    nbNeutralWords = 0
    for word in ipuContent:
        word = word.replace("\n","").lower()

        if word in specialWords:
            nbSpecialWords += 1
        if fileWithNeutralKeywords is not None:
            if word in neutralWords:
                nbNeutralWords += 1
    if len(ipuContent) - nbNeutralWords <= 0:
        return False

    if nbSpecialWords / (len(ipuContent) - nbNeutralWords) < minRatio:
        return False

    if len(ipuContent) - nbNeutralWords > maxSize:
        return False

    return True
