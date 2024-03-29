#!/usr/bin/env python3

import glob,hashlib,os,sqlite3

DEFAULT_DIR="./"
DIR=DEFAULT_DIR
BUFFER_LIMIT = 1000000000

database = sqlite3.connect("database.db")
cursor = database.cursor()


#create a table if doesnt already exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hashdb'")
if not cursor.fetchone():
    cursor.execute("""CREATE TABLE hashdb (hash TEXT, filename TEXT, duplicates TEXT)""")
    database.commit()




files = glob.glob("**",recursive=True)
#print(files)


for filename in files:
    if os.path.isdir(filename):
        continue
    filesize = os.path.getsize(filename)
    if filesize == 0:
        filename_hash = 0
        continue
    myPict = open(filename, 'rb')
    hasher = hashlib.md5()
    buf = myPict.read(BUFFER_LIMIT)
    hasher.update(buf)

    
    filename_hash = hasher.hexdigest()
    
    cursor.execute("SELECT filename,hash,duplicates FROM hashdb WHERE hash=?",(filename_hash,))
    output = cursor.fetchall()

    if not output : 
        cursor.execute("INSERT into hashdb VALUES (?,?,?)",(filename_hash,filename,""))
        database.commit()


    elif filename != output[0][0] :
       print(filename, "is a duplicate of ", output[0][0])
       duplicates_field = output[0][2]+ " " + filename
       cursor.execute("UPDATE hashdb SET duplicates=? WHERE filename=?",(duplicates_field,output[0][0]))
       database.commit()
    myPict.close()


cursor.close()
database.close()
