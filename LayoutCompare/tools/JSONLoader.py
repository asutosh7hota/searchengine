from model import Element
from model import Layout
import json
import os

def loadJSONFile(fileName) -> Layout:
    with open(fileName, "r") as read_file:
        data = Layout()
        JSONdata = json.load(read_file).get("layouts")[0]
        data.canvasWidth = JSONdata.get('canvasWidth')
        data.canvasHeight = JSONdata.get('canvasHeight')
        data.id = JSONdata.get('id')
        if data.id is None:
            data.id = os.path.basename(fileName)

        JSONelements = JSONdata.get('elements')
        data.N = len(JSONelements)
        
        for JSONelement in JSONelements:
            element = Element()
            element.id = JSONelement.get('id')
            element.X = JSONelement.get('x')
            element.Y = JSONelement.get('y')
            element.width = JSONelement.get('width')
            element.height = JSONelement.get('height')
            data.elements.append(element)

    return data