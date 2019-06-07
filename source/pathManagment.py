import os.path

def getOriginePath():
    return os.path.join(os.path.dirname(__file__), "..")

def getTextPath():
    return os.path.join(getOriginePath(), "txt")

def getPathToSerialized():
    return os.path.join(getOriginePath(), "serialized")

def getSimoneOutputPath():
    return os.path.join(getOriginePath(),"source", "Simone", "output")
