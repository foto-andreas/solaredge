#!/usr/bin/env python

# Maintain a file containing the current state of SolarEdge inverters and optimizers

import json
import getopt
import time
import sys

# get program arguments and options
(opts, args) = getopt.getopt(sys.argv[1:], "o:")
try:
    inFile = open(args[0])
except:
    inFile = sys.stdin
for opt in opts:
    if opt[0] == "-o":
        outFileName = opt[1]
        
# initialize the state from the file if it exists
try:
    with open(outFileName) as stateFile:
        stateDict = json.load(stateFile)
except:
    stateDict = {"inverters": {}, "optimizers": {}}
        

# initialize empty reminder dictionary
lastDict = {"optimizers": {}}
aggregatedDict = {"optimizers": {}}
# read the input forever
while True:
    jsonStr = ""
    # wait for data
    while jsonStr == "":
        time.sleep(.1)
        jsonStr = inFile.readline()
    inDict = json.loads(jsonStr)
    # check for resetted optimizers and handle uptime and eday for them
    for optimizer in inDict["optimizers"].keys():
        if optimizer in lastDict["optimizers"]:
            if inDict["optimizers"][optimizer]["Date"] == stateDict["optimizers"][optimizer]["Date"]:
                if int(inDict["optimizers"][optimizer]["Uptime"]) < int(stateDict["optimizers"][optimizer]["Uptime"]):
                    if optimizer in aggregatedDict["optimizers"].keys():
                        aggregatedDict["optimizers"][optimizer]["Uptime"] += lastDict["optimizers"][optimizer]["Uptime"]
                        aggregatedDict["optimizers"][optimizer]["Eday"] += lastDict["optimizers"][optimizer]["Eday"]
                    else:
                        aggregatedDict["optimizers"][optimizer] = lastDict["optimizers"][optimizer].copy()
    	lastDict["optimizers"][optimizer] = inDict["optimizers"][optimizer].copy()
    # update the state values
    stateDict["inverters"].update(inDict["inverters"])
    stateDict["optimizers"].update(inDict["optimizers"])

    # update the state file width the current and aggregated values
    with open(outFileName, "w") as outFile:
        tempDict = {"inverters": {}, "optimizers": {}}
        tempDict["inverters"] = stateDict["inverters"]
        for optimizer in stateDict["optimizers"].keys():
            tempDict["optimizers"][optimizer] = stateDict["optimizers"][optimizer].copy();
            if optimizer in aggregatedDict["optimizers"].keys():
                tempDict["optimizers"][optimizer]["Uptime"] += aggregatedDict["optimizers"][optimizer]["Uptime"]
	        tempDict["optimizers"][optimizer]["Eday"] += aggregatedDict["optimizers"][optimizer]["Eday"]
        json.dump(tempDict, outFile)
