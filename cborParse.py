import cbor
import re
import os
import json
import traceback

#location where the CBOR files are present
rootdir="/Volumes/Blunder/latest_commoncrawl/crawl"
strin=""
outputJson={}
countfiles=0
setOfKeywords={}
setOfString={}

#dirwalk
for root, subFolders, files in os.walk(rootdir):
    for fileName in files:
        rec={}
        keyword=""
        status=""
        content_Type=""
        count=0

        if re.match(r'^\.', fileName):
            continue
        if re.match(r'.*.json$',fileName):
            continue
        if re.match(r'.*.py$',fileName):
            continue
        if re.match(r'.*.(sh|txt)$',fileName):
            continue

        # if countfiles==50:
        #     break
        try:
            with open(os.path.join(root,fileName), 'r') as temp:
                rec=cbor.load(temp)
                d = json.loads(rec)

                content_Type=d["response"]["headers"][1][1]
                if ";" in content_Type:
                    content_Type=content_Type.split(";")[0]
                if d["response"]["status"]=="" or d["response"]["status"]=="200":
                    status="200"
                    if "=" in d["url"]:
                        keyword=d["url"].split("=")[1]
                    else:
                        continue
                    if keyword.lower() in d["response"]["body"].lower():
                        count=d["response"]["body"].count(keyword)
                    else:
                        continue
                    if keyword in setOfKeywords:
                        setOfKeywords[keyword]=count+setOfKeywords[keyword]
                        setOfString[keyword]=status+"-"+content_Type+"-"+keyword+","+str(count)+"\n"
                    else:
                        setOfKeywords[keyword]=count
                        setOfString[keyword]=status+"-"+content_Type+"-"+keyword+","+str(count)+"\n"
                else:
                    strin+=status+"-"+content_Type
                print countfiles
                countfiles+=1
        except:
            traceback.print_exc()
            continue
    # if(countfiles==50):
    #     break
for key in setOfString:
    strin+=setOfString[key]

outputJson["data"]=strin

print outputJson
with open("output.json",'w+') as outtemp:
    json.dump(outputJson,outtemp)
