import pandas as pd
import numpy as np
import requests
import json
import myFunctions as mf
import base64

def stageOne(endpointUrl, tmpFolderLocation):
    dataString=requests.get(endpointUrl).content
    myData=pd.read_csv(io.StringIO(dataString.decode('utf-8')))
    
    #Do the actual magic
    myResult = mf.start_at_A(myData)

    print(myResult)

    f = open(tmpFolderLocation + '/randomBytes', 'wb')
    f.write(myResult["randomBytes"])
    f.close()

    del myResult["randomBytes"]

    myResult["matrixBytes"] = str(base64.b64encode(myResult["matrixBytes"]))
    myResult["sumNoiseBytes"] = str(base64.b64encode(myResult["sumNoiseBytes"]))

    return myResult

def stageTwo():
    return {"test": "two"}

def stageThree():
    return {"test": "three"}

def stageFour():
    return {"test": "four"}