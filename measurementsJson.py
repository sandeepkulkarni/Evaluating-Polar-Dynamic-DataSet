__author__ = 'AravindMac'

from os import listdir
import json
import operator
import re

if __name__ == '__main__':
    inputPath = "/Users/AravindMac/Desktop/polardata_json/text_html"
    measurementDict = {}
    count=0
    for file in listdir(inputPath):
        try:
            if(file!=".DS_Store" and count < 3000):
                count+=1
                if count%100 == 0:
                    print count
                with open(inputPath+"/"+file, "r") as data_file:
                    data = json.load(data_file)
                    #print(data.keys())
                    #break
                    if "STANFORD_NER" in data:
                        measurements = data["STANFORD_NER"][0]["MEASUREMENT"]
                        for measurement in measurements:
                            measurement = measurement.encode("ascii")
                            match = re.match(r"([0-9]+)([a-z]+)", measurement, re.I)
                            if match:
                                items = match.groups()
                                if items[1] in measurementDict:
                                    measurementDict[items[1]]["values"].append(int(items[0]))
                                    measurementDict[items[1]]["min"] = min(measurementDict[items[1]]["values"])
                                    measurementDict[items[1]]["max"] = max(measurementDict[items[1]]["values"])
                                    measurementDict[items[1]]["range"] = measurementDict[items[1]]["max"] - measurementDict[items[1]]["min"]
                                    measurementDict[items[1]]["mean"] = sum(measurementDict[items[1]]["values"])/len(measurementDict[items[1]]["values"])
                                else:
                                    measurementDict[items[1]]={}
                                    measurementDict[items[1]]["values"]=[]
                                    measurementDict[items[1]]["values"].append(int(items[0]))
                                    measurementDict[items[1]]["min"] = items[0]
                                    measurementDict[items[1]]["max"] = items[0]
                                    measurementDict[items[1]]["range"] = measurementDict[items[1]]["max"] - measurementDict[items[1]]["min"]
                                    measurementDict[items[1]]["mean"] = items[0]

        except:
            continue

    print({"text/html":measurementDict})
    with open('wordCloud.json', 'w') as f:
        json.dump(measurementDict, f)

    #f.write(str({"application/pdf":measurementDict}))

