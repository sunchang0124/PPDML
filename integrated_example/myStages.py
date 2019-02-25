import pandas as pd
import numpy as np
import requests
import json
import myFunctions as mf
import base64

def stageOne(endpointUrl, tmpFolderLocation):
    #dataString=requests.get(endpointUrl).text
    myData=pd.read_csv(endpointUrl)
    
    #Do the actual magic
    myResult = mf.start_at_A(myData)

    f = open(tmpFolderLocation + '/randomBytes', 'wb')
    f.write(myResult["randomBytes"])
    f.close()

    del myResult["randomBytes"]

    myResult["matrixBytes"] = base64.b64encode(myResult["matrixBytes"])
    myResult["sumNoiseBytes"] = base64.b64encode(myResult["sumNoiseBytes"])

    return myResult

def stageTwo(endpointUrl, tmpFolderLocation, inputArgs):
    myData=pd.read_csv(endpointUrl)
    
    matrixBytes = base64.b64decode(inputArgs["matrixBytes"])
    sumNoiseBytes = base64.b64decode(inputArgs["sumNoiseBytes"])
    
    myResult = mf.start_at_B(myData, matrixBytes, sumNoiseBytes, inputArgs["divideSet"])
    
    f = open(tmpFolderLocation + '/randomBytes', 'wb')
    f.write(myResult["randomBytes"])
    f.close()

    del myResult["randomBytes"]
    
    myResult["sumNoisesAB"] = base64.b64encode(myResult["sumNoisesAB"])
    myResult["sumNoisesB"] = base64.b64encode(myResult["sumNoisesB"])
    
    return myResult

def stageThree():
    return {"test": "three"}

def stageFour():
    return {"test": "four"}