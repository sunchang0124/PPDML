import os
import json
import myStages as ms

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
    outputJson = ms.stageOne(endpointType, endpointUrl)
if currentStage == 2:
    outputJson = ms.stageTwo()
if currentStage == 3:
    outputJson = ms.stageThree()
if currentStage == 4:
    outputJson = ms.stageFour()

# Write output to file
with open(outputFileLocation, 'w') as f:
    f.write(json.dumps(outputJson))