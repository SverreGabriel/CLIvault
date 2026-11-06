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

printDatabase()
printTypes()