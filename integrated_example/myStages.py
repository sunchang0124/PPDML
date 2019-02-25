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

    f = open(tmpFolderLocation + '/randomBytes', 'w')
    f.write(json.dumps(myResult["randomBytes"]))
    f.close()

    del myResult["randomBytes"]

    return myResult

def stageTwo(endpointUrl, tmpFolderLocation, inputArgs):
    myData=pd.read_csv(endpointUrl)
    
    myResult = mf.start_at_B(myData, inputArgs["matrixBytes"], inputArgs["sumNoiseBytes"], inputArgs["divideSet"])
    
    f = open(tmpFolderLocation + '/randomBytes', 'w')
    f.write(json.dumps(myResult["randomBytes"]))
    f.close()

    del myResult["randomBytes"]
    
    return myResult

def stageThree(endpointUrl, tmpFolderLocation, inputArgs):
    myData=pd.read_csv(endpointUrl)
    
    with open(tmpFolderLocation + '/randomBytes') as binary_file:
        A_randoms = json.loads(binary_file.read())
    
    myResult = mf.communication_at_A(myData, A_randoms, inputArgs["sumNoisesAB"], inputArgs["divideSet"])
    
    return myResult

def stageFour():
    return {"test": "four"}