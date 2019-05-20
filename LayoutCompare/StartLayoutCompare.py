import sys
from tools.JSONLoader import loadJSONFile
from tools.JSONDisplay import actualDisplay
from solver.PrepareParameters import prepare
from solver.MIPCompare import solve


def findDifference(firstFile:str, secondFile:str, displayResult = False) -> int:
    firstLayout = loadJSONFile(firstFile)
    secondLayout = loadJSONFile(secondFile)
    prepare(firstLayout, secondLayout)
    if displayResult is True:
            actualDisplay(firstLayout, "FirstLayout")
            actualDisplay(secondLayout, "SecondLayout")
    return solve(firstLayout, secondLayout)

def runStandAlone():
    if(len(sys.argv)<3):
        print("SYNTAX ERROR: Please launch with two JSON files as first and argument")
        exit(-1)
    if(len(sys.argv[1])<6 or len(sys.argv[2])<6):
        print("SYNTAX ERROR: Please give full path of JSON file as first and second argument")
        exit(-1)
    
    print("Auto result is --> ",findDifference(sys.argv[1], sys.argv[2], displayResult = True))
    
runStandAlone()