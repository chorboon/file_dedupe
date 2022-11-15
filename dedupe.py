#!/usr/bin/env python3

import glob,hashlib,os

DEFAULT_DIR="./"
DIR=DEFAULT_DIR + "*"


files = glob.glob(DIR, recursive=True)
print(files)

fileDict ={}
#myFile = open('sample.txt','w')

for filename in files:
    if os.path.isdir(filename):
        continue
    myPict = open(filename, 'rb')
    hasher = hashlib.md5()
    buf = myPict.read()
    hasher.update(buf)

    
#    filename_hash = hasher.hexdigest()
    if not fileDict.get(hasher.hexdigest()): 
       fileDict[hasher.hexdigest()] = filename
    else :
       print(filename, "is a duplicate")
#    myFile.write(str(fileDict))
    print(filename)
    myPict.close()

print(fileDict.items())
#myFile.close()