__author__ = 'rrgirish'

import solr
import os
import sys
import json

s = solr.SolrConnection('http://localhost:8983/solr/polardata')
inputdir="/Volumes/Blunder/polardata_sorted"

outputJson=[]
for root, dirs, files in os.walk(inputdir):
    for dir in dirs:
        dict1={}
        dict2={}
        print(dir)

        #print(sum(os.path.getsize(f) for f in os.listdir(os.path.join(root,dir)) if os.path.isfile(f)))
        dirsize=sum( os.path.getsize(os.path.join(root,dirpath,filename)) for dirpath, dirnames, filenames in os.walk( os.path.join(root,dir) ) for filename in filenames )
        res=s.select("ContentType:"+dir,rows="2147483647") #
        size=0
        for hit in res.results:
            size+=sys.getsizeof(hit)
        dict1["mimeType"]=dir.replace("_","/")
        dict1["size"]=size
        dict1["source"]="solr"

        dict2["mimeType"]=dir.replace("_","/")
        dict2["size"]=dirsize
        dict2["source"]="file"

        outputJson.append(dict1)
        outputJson.append(dict2)
        print outputJson

with open("output.json",'w+') as outtemp:
    json.dump(outputJson,outtemp)

print outputJson
