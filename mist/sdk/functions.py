import tempfile
import re
import xml.etree.ElementTree as ET

from mist.sdk.config import config

def tmpFileFunction():
    return tempfile.NamedTemporaryFile(delete=False).name

def rangeFunction(begin, end, step):
    return list(range(begin, end, step))

def searchInText(regex: str, text: str):
    try:
        if re.findall(regex, text):
            return True
    except Exception as e:
        print(f" Error in 'BuiltSearchInText' -> {e}")
    return False

def searchInXML(xpath: str, text: str):
    try:
        root = ET.fromstring(text)
        found = root.findall(xpath)
    except Exception as e:
        print(f" Error in 'BuiltSearchInXML' -> {e}")
        return False
    return [ {"text": e.text, "attributes": e.attrib } for e in found ] if found is not None else []

class _Functions(dict):

    def __init__(self):
        super(_Functions, self).__init__()
        self["tmpFile"] = {"native": True, "commands": tmpFileFunction}
        self["range"] = {"native": True, "commands": rangeFunction}
        self["searchInText"] = {"native": True, "commands": searchInText}
        self["searchInXML"] = {"native": True, "commands": searchInXML}

functions = _Functions()

__all__ = ("functions", )
