__author__ = 'AravindMac'

from os import listdir
import json

if __name__ == '__main__':

    #Input directory path
    inputPath = "/Users/AravindMac/Desktop/polardata_json_grobid/application_pdf"
    contentDict = {}
    contentLengthList = []
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
                    parser = data["meta-tags"][0]["X-Parsed-By"].encode("ascii")    #Retrieve the parser call chain
                    mimetype = data["meta-tags"][0]["Content-Type"].encode("ascii").split(";")[0]   #Retrieve the mimetype
                    length=0
                    for field in data["meta-tags"][0]:          #Loop through all the metadata fields
                        length+=len(data["meta-tags"][0][field])    #Count the number of characters present in the metadata fields.
                    if length < 100:
                        flag = 1
                    elif length >=100 and length<500:
                        flag = 2
                    elif length>=500 and length<1000:
                        flag = 3
                    elif length>1000:
                        flag = 4

                    if flag in contentDict:
                        contentDict[flag]+=1
                    else:
                        contentDict[flag]=1
        except:
            continue

    jsonList = []
    for key in contentDict.keys():
        if key == 1:                #Assign the file size for each file
            filesize = "<100"
        elif key == 2:
            filesize = "100-500"
        elif key == 3:
            filesize = "500-1000"
        elif key == 4:
            filesize = ">1000"
        jsonList.append({"mimeType":mimetype,"parser":"[org.apache.tika.parser.DefaultParser,"+parser+"]","fileSize":filesize,"count":contentDict[key]})

    print jsonList

    #Write the result to the json file
    with open('bubbleMatrixMetadata.json', 'a') as f:
        json.dump(jsonList, f)
