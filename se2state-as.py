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
lastDict = {"optimizers": {}, "inverters": {}}
aggregatedDict = {"optimizers": {}, "inverters" : {}}
# read the input forever
while True:
    jsonStr = ""
    # wait for data
    while jsonStr == "":
        time.sleep(.5)
        jsonStr = inFile.readline()
    inDict = json.loads(jsonStr)
    # check for resetted optimizers and handle uptime and eday for them
    if inDict["optimizers"] != {}
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
        # check for resetted inverters and handle uptime an eday for them
        for inverter in inDict["inverters"].keys():
            if inverter in lastDict["inverters"]:
                if inDict["inverters"][inverter]["Date"] == stateDict["inverters"][inverter]["Date"]:
                    if int(inDict["inverters"][inverter]["Uptime"]) < int(stateDict["inverters"][inverter]["Uptime"]):
                        if inverter in aggregatedDict["inverters"].keys():
                            aggregatedDict["inverters"][inverter]["Uptime"] += lastDict["inverters"][inverter]["Uptime"]
                            aggregatedDict["inverters"][inverter]["Eday"] += lastDict["inverters"][inverter]["Eday"]
                        else:
                            aggregatedDict["inverters"][inverter] = lastDict["inverters"][inverter].copy()
            lastDict["inverters"][inverter] = inDict["inverters"][inverter].copy()
        # update the state values
        stateDict["inverters"].update(inDict["inverters"])
        stateDict["optimizers"].update(inDict["optimizers"])
        # update the state file width the current and aggregated values
        with open(outFileName, "w") as outFile:
            tempDict = {"inverters": {}, "optimizers": {}}
            for optimizer in stateDict["optimizers"].keys():
                tempDict["optimizers"][optimizer] = stateDict["optimizers"][optimizer].copy();
                if optimizer in aggregatedDict["optimizers"].keys():
                    tempDict["optimizers"][optimizer]["Uptime"] += aggregatedDict["optimizers"][optimizer]["Uptime"]
	            tempDict["optimizers"][optimizer]["Eday"] += aggregatedDict["optimizers"][optimizer]["Eday"]
            for inverter in stateDict["inverters"].keys():
                tempDict["inverters"][inverter] = stateDict["inverters"][inverter].copy();
                if inverter in aggregatedDict["inverters"].keys():
                    tempDict["inverters"][inverter]["Uptime"] += aggregatedDict["inverters"][inverter]["Uptime"]
	            tempDict["inverters"][inverter]["Eday"] += aggregatedDict["inverters"][inverter]["Eday"]
            json.dump(tempDict, outFile)

