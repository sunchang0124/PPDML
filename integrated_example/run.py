import os
import json
import myFunctions as mf

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
    outputJson = mf.stageOne(endpointType, endpointUrl)
if currentStage == 2:
    outputJson = mf.stageTwo()
if currentStage == 3:
    outputJson = mf.stageThree()
if currentStage == 4:
    outputJson = mf.stageFour()

# Write output to file
with open(outputFileLocation, 'w') as f:
    f.write(json.dumps(outputJson))