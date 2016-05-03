__author__ = 'AravindMac'

from os import listdir
import json
from collections import OrderedDict

#Function to count the number of entites tagged for each word by each parser.
def countEntites(parser,entity):
    for i in range(len(data[parser][0][entity])):
        words = data[parser][0][entity][str(i)].split(" ")
        for word in words:
            word = word.encode("ascii")
            word = word.replace("'","").replace(",\.\/\;","").replace("<[A-Za-z\/]*[^>]*>", "")
            if word in entityDict.keys():
                if parser in entityDict[word]:
                    entityDict[word][parser]+=1
                else:
                    entityDict[word][parser]=1
            else:
                entityDict[word]={}
                entityDict[word][parser]=1


if __name__ == '__main__':

    #Input directory path
    inputPath = "/Users/AravindMac/Desktop/polardata_json_grobid/application_pdf"
    entityDict = {}
    count=0
    for file in listdir(inputPath):
        try:
            if(file!=".DS_Store"):
                count+=1
                if count%100 == 0:
                    print count
                if count < 1000:
                    with open(inputPath+"/"+file, "r") as data_file:
                        data = json.load(data_file)     #Load the content of the file as a json object

                        if "CoreNLP" in data:           #Count the number of entities tagged by CoreNLP parser
                            if "ORGANIZATION" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","ORGANIZATION")
                            if "LOCATION" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","LOCATION")
                            if "PERSON" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","PERSON")
                            if "DATE" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","DATE")

                        if "OpenNLP" in data:           #Count the number of entities tagged by OpenNLP parser
                            if "ORGANIZATION" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","ORGANIZATION")
                            if "LOCATION" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","LOCATION")
                            if "PERSON" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","PERSON")
                            if "DATE" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","DATE")

                        if "NLTK" in data:              #Count the number of entities tagged by NLTK parser
                            if "NAMES" in data["NLTK"][0]:
                                countEntites("NLTK","NAMES")
        except:
            continue

    #Sort the items in descending order to retrieve the most significant items
    sortedDict = OrderedDict(sorted(entityDict.items(), key=lambda (k,v):len(v), reverse=True))
    print(sortedDict)

    #Priortize the words classified by all 3 parsers.
    for key in sortedDict.keys():
        diff=[]
        if len(sortedDict[key]) == 3:
            coreNlp = sortedDict[key]["CoreNLP"]
            openNlp = sortedDict[key]["OpenNLP"]
            nltk = sortedDict[key]["NLTK"]

            diff.append(abs(coreNlp - openNlp))
            diff.append(abs(openNlp - nltk))
            diff.append(abs(coreNlp - nltk))

            sortedDict[key]["diff"]=sum(diff)
        elif len(sortedDict[key]) == 2:
            if "NLTK" not in sortedDict[key]:
                coreNlp = sortedDict[key]["CoreNLP"]
                openNlp = sortedDict[key]["OpenNLP"]
                diff.append(abs(coreNlp - openNlp))
            elif "CoreNLP" not in sortedDict[key]:
                openNlp = sortedDict[key]["OpenNLP"]
                nltk = sortedDict[key]["NLTK"]
                diff.append(abs(nltk - openNlp))
            elif "OpenNLP" not in sortedDict[key]:
                coreNlp = sortedDict[key]["CoreNLP"]
                nltk = sortedDict[key]["NLTK"]
                diff.append(abs(coreNlp - nltk))
            sortedDict[key]["diff"]=500+sum(diff)
        elif len(sortedDict[key]) == 1:
            if "NLTK" in sortedDict[key]:
                nltk = sortedDict[key]["NLTK"]
                sortedDict[key]["diff"]=1000+nltk
            elif "CoreNLP" in sortedDict[key]:
                coreNlp = sortedDict[key]["CoreNLP"]
                sortedDict[key]["diff"]=1000+coreNlp
            elif "OpenNLP" in sortedDict[key]:
                openNlp = sortedDict[key]["OpenNLP"]
                sortedDict[key]["diff"]=1000+openNlp

    #Sort the items again to get the words that were classified properly with a mutual agreement among all 3 parsers
    sortedDict = OrderedDict(sorted(sortedDict.items(), key=lambda (k,v):v["diff"]))

outerDict={}
outerDict["labels"]=[]
outerDict["series"]=[]

coreNlpDict={}
coreNlpDict["name"]="CoreNLP"
coreNlpDict["value"]=[]

openNlpDict={}
openNlpDict["name"]="OpenNLP"
openNlpDict["value"]=[]

nltkDict={}
nltkDict["name"]="NLTK"
nltkDict["value"]=[]

#Plot the stacked bar chart for the top 500 words tagged by the parsers
i=0
for key in sortedDict.keys():
    i+=1
    if i>500:
        break
    outerDict["labels"].append(key)

    if "CoreNLP" in sortedDict[key]:
        coreNlpDict["value"].append(sortedDict[key]["CoreNLP"])
    else:
        coreNlpDict["value"].append(0)

    if "OpenNLP" in sortedDict[key]:
        openNlpDict["value"].append(sortedDict[key]["OpenNLP"])
    else:
        openNlpDict["value"].append(0)

    if "NLTK" in sortedDict[key]:
        nltkDict["value"].append(sortedDict[key]["NLTK"])
    else:
        nltkDict["value"].append(0)


outerDict["series"].append(coreNlpDict)
outerDict["series"].append(openNlpDict)
outerDict["series"].append(nltkDict)
print outerDict

#Write the output to the json file
with open("ner.json","w") as f:
    json.dump(outerDict, f)
