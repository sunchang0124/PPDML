import pandas as pd
import numpy as np
import requests
import json
import myFunctions as mf
import base64

def stageOne(endpointUrl, tmpFolderLocation, Divide_set, C_seed, C_min, C_max):
    #dataString=requests.get(endpointUrl).text
    myData=pd.read_csv(endpointUrl)
    myData = myData.drop('Unnamed: 0', axis=1)
    
    #Do the actual magic
    myResult = mf.start_at_A(myData, Divide_set, C_seed, C_min, C_max)

    f = open(tmpFolderLocation + '/randomBytes', 'w')
    f.write(json.dumps(myResult["randomBytes"]))
    f.close()

    del myResult["randomBytes"]

    return myResult

def stageTwo(endpointUrl, tmpFolderLocation, inputArgs, Divide_set, C_seed, C_min, C_max):
    myData=pd.read_csv(endpointUrl)
    colB = myData.columns
    Y = myData['diag_3']
    myData = myData[colB[0:6]].drop(['Unnamed: 0'], axis=1) # we only use first 5 columns here because the values
    
    myResult = mf.start_at_B(myData, C_seed, C_min, C_max, inputArgs["sumNoiseBytes"], Divide_set)
    
    f = open(tmpFolderLocation + '/randomBytes', 'w')
    f.write(json.dumps(myResult["randomBytes"]))
    f.close()

    del myResult["randomBytes"]
    
    return myResult

def stageThree(endpointUrl, tmpFolderLocation, inputArgs, Divide_set):
    myData=pd.read_csv(endpointUrl)
    myData = myData.drop('Unnamed: 0', axis=1)
    
    with open(tmpFolderLocation + '/randomBytes') as binary_file:
        A_randoms = json.loads(binary_file.read())
    
    myResult = mf.communication_at_A(myData, A_randoms, inputArgs["sumNoisesAB"], inputArgs["sumNoisesB"], Divide_set)
    
    return myResult

def stageFour(endpointUrl, tmpFolderLocation, inputArgs, Divide_set):
    myData=pd.read_csv(endpointUrl)
    colB = myData.columns
    Y = myData['diag_3']
    myData = myData[colB[0:6]].drop(['Unnamed: 0'], axis=1) # we only use first 5 columns here because the values
    
    with open(tmpFolderLocation + '/randomBytes') as binary_file:
        B_randoms = json.loads(binary_file.read())
        
    myResult = mf.Final_at_B(myData, inputArgs["randomsSumSet"], inputArgs["sumNoisesBARand"], inputArgs["XaTXa"], B_randoms, Divide_set)
    
    return myResult