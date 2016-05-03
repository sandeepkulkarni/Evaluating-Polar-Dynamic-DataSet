__author__ = 'AravindMac'

from os import listdir
import json
import re

if __name__ == '__main__':

    #Input directory path
    inputPath = "/Users/AravindMac/Desktop/polardata_json_grobid/application_pdf"
    measurementDict = {}
    valueDict = {}
    count=0
    #Iterate through all the files listed in the directory path specified
    for file in listdir(inputPath):
        try:
            if(file!=".DS_Store"):
                count+=1
                if count%100 == 0:
                    print count
                with open(inputPath+"/"+file, "r") as data_file:
                    data = json.load(data_file)             #Load the contents of the file as a json object
                    mimetype = data["meta-tags"][0]["Content-Type"].encode("ascii").split(";")[0]   #Retrieve the mimetype
                    # Check if measurements are present in the file
                    if "STANFORD_NER" in data:
                        measurements = data["STANFORD_NER"][0]["MEASUREMENT"]
                        for measurement in measurements:
                            measurement = measurement.encode("ascii")
                            match = re.match(r"([0-9]+)([a-z]+)", measurement, re.I)    #Regular expression to separate number from string
                            if match:
                                items = match.groups()
                                measurement_number = int(items[0])      #Fetch the measurement number
                                unit = items[1].upper()         #Convert the unit to uppercase
                                if unit in ["C","F","K"]:       #Assign the category for each unit
                                    unit = "TEMPERATURE/"+str(unit)
                                elif unit in ["KG","G","MG"]:
                                    unit = "WEIGHT/"+str(unit)
                                elif unit in ["CM","MM","M","KM","FT"]:
                                    unit = "LENGTH/"+str(unit)
                                elif unit == "J":
                                    unit = "ENERGY/"+str(unit)
                                elif unit == "N":
                                    unit = "FORCE/"+str(unit)
                                elif unit == "W":
                                    unit = "POWER/"+str(unit)
                                elif unit in ["S","SEC"]:
                                    unit = "TIME/"+str(unit)
                                elif unit == "R":
                                    unit = "GAS/"+str(unit)
                                elif unit == "L":
                                    unit = "VOLUME/"+str(unit)
                                elif unit == "HZ":
                                    unit = "FREQUENCY/"+str(unit)
                                elif unit == "PA":
                                    unit = "PRESSURE/"+str(unit)

                                if unit in measurementDict:             #Compute the max,min and mean values for each unit
                                    valueDict[unit]["values"].append(measurement_number)
                                    measurementDict[unit]["min"] = min(valueDict[unit]["values"])
                                    measurementDict[unit]["max"] = max(valueDict[unit]["values"])
                                    measurementDict[unit]["mean"] = sum(valueDict[unit]["values"])/len(valueDict[unit]["values"])
                                else:
                                    measurementDict[unit]={}
                                    valueDict[unit]={}
                                    valueDict[unit]["values"]=[]
                                    valueDict[unit]["values"].append(measurement_number)
                                    measurementDict[unit]["min"] = measurement_number
                                    measurementDict[unit]["max"] = measurement_number
                                    measurementDict[unit]["mean"] = measurement_number

        except:
            continue
    jsonList = []

    #Write the result to the json file
    with open('measurements.json', 'a') as f:
        for measurement in measurementDict:
            jsonDict = {"mimetype":mimetype, "measurement":measurement, "max":measurementDict[measurement]["max"], "min":measurementDict[measurement]["min"], "mean":measurementDict[measurement]["mean"]}
            print jsonDict
            jsonList.append(jsonDict)
        json.dump(jsonList, f)

