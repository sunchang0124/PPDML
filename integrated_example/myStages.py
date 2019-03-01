import pandas as pd
import numpy as np
import requests
import json
import myFunctions as mf
import base64

def stageOne(endpointUrl, tmpFolderLocation, Divide_set, C_seed, C_min, C_max):
    #dataString=requests.get(endpointUrl).text
    myData=pd.read_csv(endpointUrl)
    
    #Do the actual magic
    myResult = mf.start_at_A(myData, Divide_set, C_seed, C_min, C_max)

    f = open(tmpFolderLocation + '/randomBytes', 'w')
    f.write(json.dumps(myResult["randomBytes"]))
    f.close()

    del myResult["randomBytes"]

    return myResult

def stageTwo(endpointUrl, tmpFolderLocation, inputArgs, Divide_set, C_seed, C_min, C_max):
    myData=pd.read_csv(endpointUrl)
    
    myResult = mf.start_at_B(myData, C_seed, C_min, C_max, inputArgs["sumNoiseBytes"], Divide_set)
    
    f = open(tmpFolderLocation + '/randomBytes', 'w')
    f.write(json.dumps(myResult["randomBytes"]))
    f.close()

    del myResult["randomBytes"]
    
    return myResult

def stageThree(endpointUrl, tmpFolderLocation, inputArgs, Divide_set):
    myData=pd.read_csv(endpointUrl)
    
    with open(tmpFolderLocation + '/randomBytes') as binary_file:
        A_randoms = json.loads(binary_file.read())
    
    myResult = mf.communication_at_A(myData, A_randoms, inputArgs["sumNoisesAB"], Divide_set)
    
    return myResult

def stageFour(endpointUrl, tmpFolderLocation, inputArgs, Divide_set):
    myData=pd.read_csv(endpointUrl)
    
    with open(tmpFolderLocation + '/randomBytes') as binary_file:
        B_randoms = json.loads(binary_file.read())
        
    myResult = mf.Final_at_B(myData, inputArgs["randomsSumSet"], inputArgs["sumNoisesBARand"], inputArgs["XaTXa"], inputArgs["sumNoisesAB"], B_randoms, Divide_set)
    
    return myResult