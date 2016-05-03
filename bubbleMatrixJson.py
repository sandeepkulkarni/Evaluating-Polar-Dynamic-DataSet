__author__ = 'AravindMac'

from os import listdir
import json

if __name__ == '__main__':
    inputPath = "/Users/AravindMac/Desktop/polardata_json/text_html_test"
    contentDict = {}
    contentLengthList = []
    count=0
    for file in listdir(inputPath):
        try:
            if(file!=".DS_Store"):
                count+=1
                if count%100 == 0:
                    print count
                with open(inputPath+"/"+file, "r") as data_file:
                    data = json.load(data_file)
                    parser = data["meta-tags"][0]["X-Parsed-By"].encode("ascii")
                    #print len(data["meta-tags"][0])
                    mimetype = data["meta-tags"][0]["Content-Type"].encode("ascii")
                    length = len(data["content"])
                    if length < 1000:
                        flag = 1
                    elif length >=1000 and length<5000:
                        flag = 2
                    elif length>=5000 and length<10000:
                        flag = 3
                    elif length>10000:
                        flag = 4

                    if flag in contentDict:
                        contentDict[flag]+=1
                    else:
                        contentDict[flag]=1
        except:
            continue

    jsonList = []
    for key in contentDict.keys():
        if key == 1:
            filesize = "<1000"
        elif key == 2:
            filesize = "1000-5000"
        elif key == 3:
            filesize = "5000-10000"
        elif key == 4:
            filesize = ">10000"
        jsonList.append({"mimeType":mimetype,"parser":"[org.apache.tika.parser.DefaultParser,"+parser+"]","fileSize":filesize,"count":contentDict[key]})

    print jsonList
    with open('bubbleMatrix.json', 'a') as f:
        json.dump(jsonList, f)
