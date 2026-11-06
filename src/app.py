import sqlite3
import os
from cryptography.fernet import Fernet
from db import inpRemove, inpAdd, printDatabase, printTypes


con = sqlite3.connect("vault.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS secrets(name TEXT PRIMARY KEY UNIQUE, type TEXT, value TEXT)")

if "ENCRYPTION_KEY" not in os.environ:
    key = Fernet.generate_key()
    os.environ["ENCRYPTION_KEY"] = str(key)

print("")
print("Welcome to your own personal CLIvault!!")
print("---------------------------------------")

running = True

while running:
    print("What do you want to do?")
    print("")
    print("ADD - add an entry")
    print("REMOVE - remove an entry")
    print("PRINT - print all the entries")
    print("TYPES - print all the unique types of entries you have")
    print("QUIT - quit the aplication")
    print("")

    inp = input("Type here: ").capitalize()

    if inp == "ADD":
        inpAdd()
    elif inp == "REMOVE":
        inpRemove()
    elif inp == "PRINT":
        printDatabase()
    elif inp == "TYPES":
        printTypes()
    elif inp == "QUIT":
        running = False
    else:
        print("Unnknown command please try again.")

    