import os
import json

endpointType = os.environ.get("endpointType")
endpointUrl = os.environ.get("endpointUrl")
inputFileLocation = "/input.txt"
outputFileLocation = "/output.txt"
logFileLocation = "/log.txt"
tempFolder = "/temp/"

#Read input file
with open(inputFileLocation) as f:
    inputArgs = json.load(f)

#############################################
#do whatever you want from here
#############################################
currentStage = inputArgs["stage"]
print("Stage: %s" % currentStage)

if currentStage == 1:
    #Do run 1
if currentStage == 2:
    #Do run 2
if currentStage == 3:
    #Do run 3
if currentStage == 4:
    #Do run 4

outputJson = {"endpointType": endpointType, "endpointUrl": endpointUrl }

# Write output to file
with open('output.txt', 'w') as f:
    f.write(json.dumps(outputJson))