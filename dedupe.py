#!/usr/bin/env python3

import glob,hashlib,os,sqlite3

DEFAULT_DIR="./"
DIR=DEFAULT_DIR + "*"

database = sqlite3.connect("database.db")
cursor = database.cursor()

#create a table if doesnt already exit
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hashdb'")
if not cursor.fetchone():
    cursor.execute("""CREATE TABLE hashdb (hash TEXT, filename TEXT)""")
    database.commit()




files = glob.glob(DIR, recursive=True)
print(files)


for filename in files:
    if os.path.isdir(filename):
        continue
    myPict = open(filename, 'rb')
    hasher = hashlib.md5()
    buf = myPict.read()
    hasher.update(buf)

    
    filename_hash = hasher.hexdigest()
    print(filename_hash)
    cursor.execute("SELECT filename,hash FROM hashdb WHERE hash=?",(filename_hash,))
    output = cursor.fetchall()

    if not output : 
        cursor.execute("INSERT into hashdb VALUES (?,?)",(filename_hash,filename))
        database.commit()


    elif filename != output[0][0] :
       print(filename, "is a duplicate of ", output[0][0])

    myPict.close()


cursor.close()
database.close()