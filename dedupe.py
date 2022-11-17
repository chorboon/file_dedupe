#!/usr/bin/env python3

import glob,hashlib,os,sqlite3

DEFAULT_DIR="./"
DIR=DEFAULT_DIR + "*"

database = sqlite3.connect("database.db")
cursor = database.cursor()

#create a table
#if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hash_DB'"):
#cursor.execute("""CREATE TABLE hashdb (hash TEXT, filename TEXT)""")




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

    
    filename_hash = hasher.hexdigest()
    cursor.execute("INSERT into hashdb VALUES (?,?)",(filename_hash,filename))
    database.commit()
    if not fileDict.get(filename_hash): 
       fileDict[filename_hash] = filename

    else :
       print(filename, "is a duplicate")

    print(filename)
    myPict.close()

print(fileDict.items())
#myFile.close()
cursor.close()
database.close()