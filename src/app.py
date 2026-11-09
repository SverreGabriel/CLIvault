import sqlite3
import os
from cryptography.fernet import Fernet
from pathlib import Path
from dotenv import load_dotenv
from db import inpRemove, inpAdd, printDatabase, printTypes


con = sqlite3.connect("vault.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS secrets(name TEXT PRIMARY KEY UNIQUE, type TEXT, value TEXT)")

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

key = os.getenv("ENCRYPTION_KEY")

if key is None:
    key = Fernet.generate_key().decode("utf-8")

    with open(env_path, "a", encoding="utf-8") as f:
        f.write(f"\nENCRYPTION_KEY={key}\n")

encryption_key = Fernet(key.encode("utf-8"))


print("\nWelcome to your own personal CLIvault!!")
print("---------------------------------------")

running = True

while running:
    print("What do you want to do?\n")
    print("ADD - add an entry")
    print("REMOVE - remove an entry")
    print("PRINT - print all the entries")
    print("TYPES - print all the unique types of entries you have")
    print("QUIT - quit the aplication\n")

    inp = input("Type here: ").upper()
    print("")
    

    if inp == "ADD":
        inpAdd(encryption_key)
        input("")
    elif inp == "REMOVE":
        inpRemove()
        input("")
    elif inp == "PRINT":
        printDatabase(encryption_key)
        input("")
    elif inp == "TYPES":
        printTypes()
        input("")
    elif inp == "QUIT":
        running = False
    else:
        print("Unnknown command please try again.")
        input("")

    