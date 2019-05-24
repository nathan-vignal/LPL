import os
def getSpeakers(pathToMetadata, speakerDataToRead):
    """
    only handle SWBD metadata for now
    :param pathToMetadata: 
    :param speakerDataToRead: 
    :return: 
    """
    # associating each conversation with two speakers and a topic
    f1 = open(os.path.join(pathToMetadata, "conv_tab.csv"), "r")
    lines = f1.readlines()
    convMap = {}
    for i in range(1, len(lines)):
        line = lines[i].split(',')  # eg : 2001,Y,1020,1044,303,0,910304,1218,1222, ,
        convMap[line[0]] = [line[2], line[3], line[4]]
    f1.close()

    # creating each speaker from the speakers file
    f1 = open(os.path.join(pathToMetadata, "caller_tab.csv"), "r")
    lines = f1.readlines()
    indexToRead = {}
    words = lines[0].split(',')
    for i in range(0, len(words)):
        if words[i] in speakerDataToRead:
            indexToRead[i] = words[i]
    speakers = {}
    for i in range(1, len(lines)):
        splittedLine = lines[i].split(',')  # eg : 2001,Y,1020,1044,303,0,910304,1218,1222, ,
        speakerInfos = {}
        for j in range(1, len(splittedLine)):
            if j in indexToRead:
                if indexToRead[j] == "age":
                    speakerInfos[indexToRead[j]] = str(1990 - int(splittedLine[j]))  # 1990 is that date at which the
                    # recordings took place
                    continue
                speakerInfos[indexToRead[j]] = splittedLine[j]
        speakers[splittedLine[0]] = speakerInfos
    f1.close()
    return convMap, speakers
    # speakers look like {{'1000': {'sex': 'FEMALE', 'age': '1954', 'geog...
    # convMap look like {'2001': ['1020', '1044', '303'],..
