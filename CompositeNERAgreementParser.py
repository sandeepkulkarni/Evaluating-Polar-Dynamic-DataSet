__author__ = 'AravindMac'

from os import listdir
import json
from collections import OrderedDict


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

    inputPath = "/Users/AravindMac/Desktop/polardata_json_grobid/application_pdf"
    entityDict = {}
    count=0
    for file in listdir(inputPath):
        try:
            if(file!=".DS_Store"):
                count+=1
                if count%100 == 0:
                    print count
                if count < 100:
                    with open(inputPath+"/"+file, "r") as data_file:
                        data = json.load(data_file)

                        if "CoreNLP" in data:
                            if "ORGANIZATION" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","ORGANIZATION")
                            if "LOCATION" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","LOCATION")
                            if "PERSON" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","PERSON")
                            if "DATE" in data["CoreNLP"][0]:
                                countEntites("CoreNLP","DATE")

                        if "OpenNLP" in data:
                            if "ORGANIZATION" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","ORGANIZATION")
                            if "LOCATION" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","LOCATION")
                            if "PERSON" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","PERSON")
                            if "DATE" in data["OpenNLP"][0]:
                                countEntites("OpenNLP","DATE")

                        if "NLTK" in data:
                            if "NAMES" in data["NLTK"][0]:
                                countEntites("NLTK","NAMES")

        except:
            continue
    sortedDict = OrderedDict(sorted(entityDict.items(), key=lambda (k,v):len(v), reverse=True))
    print(sortedDict)
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
            #sortedDict[key]["diff"]=sum(diff)
        elif len(sortedDict[key]) == 1:
            if "NLTK" in sortedDict[key]:
                nltk = sortedDict[key]["NLTK"]
                sortedDict[key]["diff"]=1000+nltk
                #sortedDict[key]["diff"]=nltk
            elif "CoreNLP" in sortedDict[key]:
                coreNlp = sortedDict[key]["CoreNLP"]
                sortedDict[key]["diff"]=1000+coreNlp
                #sortedDict[key]["diff"]=coreNlp
            elif "OpenNLP" in sortedDict[key]:
                openNlp = sortedDict[key]["OpenNLP"]
                sortedDict[key]["diff"]=1000+openNlp
                #sortedDict[key]["diff"]=openNlp
        #print(sortedDict[key])
    

    sortedDict = OrderedDict(sorted(sortedDict.items(), key=lambda (k,v):v["diff"]), reverse=True)

    #sorted_x = sorted(entityDict.items(), key=operator.itemgetter(1))
    #for key in sortedDict.keys():
     #   print sortedDict[key]

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

i=0
for key in sortedDict.keys():
    i+=1
    if i>100:
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
with open("ner.json","w") as f:
    json.dump(outerDict, f)
