__author__ = 'AravindMac'

from os import listdir
import json
import operator

if __name__ == '__main__':
    inputPath = "/Users/AravindMac/Desktop/polardata_json_grobid/application_pdf"
    wordDict = {}
    count=0
    for file in listdir(inputPath):
        try:
            if(file!=".DS_Store" and count < 3000):
                count+=1
                if count%100 == 0:
                    print count
                with open(inputPath+"/"+file, "r") as data_file:
                    data = json.load(data_file)
                    #pprint(data.keys())
                    #break
                    if "Language" in data:
                        language = data["Language"].encode("ascii")
                        if language in wordDict:
                            wordDict[language]+=1
                        else:
                            wordDict[language]=1
                    if "SWEET" in data:
                        if "REPRESENTATION" in data["SWEET"][0]:
                            representation = data["SWEET"][0]["REPRESENTATION"]
                            if "REPRESENTATION" in wordDict:
                                wordDict["REPRESENTATION"]+=1
                            else:
                                wordDict["REPRESENTATION"]=1
                            for word in representation:
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "REALM" in data["SWEET"][0]:
                            realm = data["SWEET"][0]["REALM"]
                            if "REALM" in wordDict:
                                wordDict["REALM"]+=1
                            else:
                                wordDict["REALM"]=1
                            for word in realm:
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "MATTER" in data["SWEET"][0]:
                            matter = data["SWEET"][0]["MATTER"]
                            if "MATTER" in wordDict:
                                wordDict["MATTER"]+=1
                            else:
                                wordDict["MATTER"]=1
                            for word in matter:
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "HUMAN ACTIVITIES" in data["SWEET"][0]:
                            humanActivities = data["SWEET"][0]["HUMAN ACTIVITIES"]
                            if "HUMAN ACTIVITIES" in wordDict:
                                wordDict["HUMAN ACTIVITIES"]+=1
                            else:
                                wordDict["HUMAN ACTIVITIES"]=1
                            for word in humanActivities:
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "PROCESS" in data["SWEET"][0]:
                            process = data["SWEET"][0]["PROCESS"]
                            if "PROCESS" in wordDict:
                                wordDict["PROCESS"]+=1
                            else:
                                wordDict["PROCESS"]=1
                            for word in process:
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "PHENOMENA" in data["SWEET"][0]:
                            phenomena = data["SWEET"][0]["PHENOMENA"]
                            if "PHENOMENA" in wordDict:
                                wordDict["PHENOMENA"]+=1
                            else:
                                wordDict["PHENOMENA"]=1
                            for word in phenomena:
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                    if "TIKA_NER" in data:
                        if "ORGANIZATION" in data["TIKA_NER"][0]:
                            organization = data["TIKA_NER"][0]["ORGANIZATION"]
                            for key in organization:
                                word = organization[key]
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "LOCATION" in data["TIKA_NER"][0]:
                            location = data["TIKA_NER"][0]["LOCATION"]
                            for key in location:
                                word = location[key]
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
                        if "PERSON" in data["TIKA_NER"][0]:
                            person = data["TIKA_NER"][0]["PERSON"]
                            for key in person:
                                word = person[key]
                                word = word.encode("ascii").upper()
                                if(word.isdigit() == False):
                                    if word in wordDict:
                                        wordDict[word]+=1
                                    else:
                                        wordDict[word]=1
        except:
            continue

sortedDict = sorted(wordDict.items(), key=operator.itemgetter(1),reverse=True)[:100]

jsonList = []
for i in range(100):
    jsonList.append({"text":sortedDict[i][0],"freq":sortedDict[i][1]})

with open('wordCloud.json', 'w') as f:
     json.dump(jsonList, f)
