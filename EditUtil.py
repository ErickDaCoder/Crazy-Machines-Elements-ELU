import sqlite3
import lzma
choice = input("""Crazy Machines Elements editor levels utility version 1.2
REMEMBER TO NEVER CLOSE THIS APPLICATION USING THE TOOLBAR!!!!
Here are the options: 
1. Backup a level (type 1),
2. Delete a level stored in the database (type 2),
3. Restore a level from the database (type 3),
4. List levels stored in the database (type 4),
5. Delete all levels stored in the database (type 5),
6. Backup all levels (type 6),
7. Rename a level in the database (type 7),
8. Reset the database (type 8)\n""")

database = sqlite3.connect("leveldb.db")
database_cursor = database.cursor()
database_cursor.execute("CREATE TABLE IF NOT EXISTS levels (\"levelname\" TEXT, \"leveldata\" BLOB)")

if choice=="1":
    levelname = "level0" + str(int(input("Level number to save:\n"))-1) + ".cml"
    with open(levelname, "rb") as level_file_handler:
        name_in_db = input("What should the level be called in the database?\n")
        database_cursor.execute("INSERT INTO \"levels\"(\"levelname\", \"leveldata\") VALUES (?, ?)", (name_in_db, lzma.compress(level_file_handler.read())))
elif choice=="2":
    database_cursor.execute("DELETE FROM levels WHERE levelname=\""+input("Level name to delete: ")+"\"")
elif choice=="3":
    name_in_db = input("Level name to restore: ")
    levelnumber = input("Level number to replace (Will delete that level if the level already exists): ")
    levelname = "level0"+str(int(levelnumber)-1) + ".cml"
    with open(levelname, "wb") as level_file_handler:
        database_cursor.execute("SELECT leveldata FROM levels WHERE levelname=\""+name_in_db+"\"")
        level_file_handler.write(lzma.decompress(database_cursor.fetchone()[0]))
elif choice=="4":
    for levelname in database_cursor.execute("SELECT levelname FROM levels"):
        print(levelname[0]+"\n")
elif choice=="5":
    database_cursor.execute("DROP TABLE levels")
    database_cursor.execute("CREATE TABLE levels (\"levelname\" TEXT, \"leveldata\" BLOB)")
elif choice=="6":
    from time import gmtime, strftime
    levelcount = input("How many levels are there?\n")
    for i in range(1, int(levelcount) + 1):
        try:
            with open("level0"+str(int(i)-1) + ".cml", "rb") as level_file_handler:
                # name_in_db = strftime("%a, %b %d %Y %H:%M:%S", gmtime()) + " (Level " + str(i) + " in mass backup)"
                cme_level_name = level_file_handler.read(51)[23:]
                cme_level_name_end_index = cme_level_name.find(b'\x00\x00\x00\x16\x00')
                cme_level_name = cme_level_name[0:cme_level_name_end_index]
                cme_level_name = cme_level_name.replace(b'\x00',b'')
                print(cme_level_name)
                cme_level_name = cme_level_name.decode()
                name_in_db = cme_level_name + "(" + strftime("%a, %b %d %Y %H:%M:%S", gmtime()) + ", level " + str(i) + " in mass backup)"

                print("Compressing level " + str(i) + " and adding to database...")
                database_cursor.execute("INSERT INTO \"levels\"(\"levelname\", \"leveldata\") VALUES (?, ?)",
                                        (name_in_db, lzma.compress(level_file_handler.read())))
                print("Done archiving level " + str(i) + ".")
        except FileNotFoundError:
            input("Level #"+str(i)+" does not exist. Nothing has been added to the database. Press enter to exit.")
            exit()
elif choice=="7":
    current_level_name=input("Current level name in database:\n")
    new_level_name=input("New level name:\n")
    database_cursor.execute("UPDATE levels SET levelname=\""+new_level_name+"\" WHERE levelname=\""+current_level_name+"\"")
elif choice=="8":
    with open("leveldb.db","wb") as A:
        A.write(lzma.decompress(b'\xfd\x37\x7a\x58\x5a\x00\x00\x04\xe6\xd6\xb4\x46\x02\x00\x21\x01\x16\x00\x00\x00\x74\x2f\xe5\xa3\xe0\x1f\xff\x00\xae\x5d\x00\x29\x94\x45\x9d\x60\xc8\x19\xf8\x26\x64\x88\x8e\x26\xfe\x31\x95\xfd\xc7\x87\x80\x06\x97\xbb\xec\x7f\xa8\x09\x7d\xbe\xf1\x9a\x93\x8c\xab\x36\xb4\xd9\xc8\xce\xac\x45\xe9\xfb\x98\xb0\x46\x94\xa5\xd1\x7a\xd9\x0f\xb5\xaa\xc6\x3d\xdd\xa7\xa7\xa9\x4b\x00\x44\x54\x2d\x82\xa8\xeb\xa9\x97\xed\x84\x08\x51\x3c\xaf\x77\x46\xb0\xd7\x56\x7d\x3f\x84\x3b\x20\x8a\x53\xe7\xf2\x69\xe5\x6f\x8e\xc6\xea\xc0\x21\x91\x02\xd4\xa8\xe0\x84\x2e\xc5\xc5\x47\x4a\xe9\x94\xad\xee\x2f\x5a\xe3\xec\xee\xd6\x3c\x3a\x7b\xab\xda\x1a\x03\x0a\x9c\x2e\x5e\xfb\x4d\xc8\x6e\x79\x59\xc1\xf3\xf0\xdf\x2d\x71\x90\x07\x6f\x31\x2d\x35\xc6\x43\x8f\x51\x3b\x4d\x62\x58\xac\x87\xc7\x64\x6e\x0d\x51\x76\x13\x50\xcf\xae\xf2\x37\xd9\xc8\x2d\x00\x00\x00\x00\xf1\x47\x49\x13\xbe\x42\x99\xf9\x00\x01\xca\x01\x80\x40\x00\x00\x44\xfb\x85\xd3\xb1\xc4\x67\xfb\x02\x00\x00\x00\x00\x04\x59\x5a'))
else:
    print("Invalid option.")

database.commit()
database.close()
input("Press enter to exit.")