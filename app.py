import sqlite3
import os
from dotenv import load_dotenv, find_dotenv
from cryptography.fernet import Fernet


con = sqlite3.connect("vault.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS secrets(name TEXT PRIMARY KEY UNIQUE, type TEXT, value TEXT)")

if "ENCRYPTION_KEY" in os.environ:
    key = Fernet.generate_key()
    os.environ["ENCRYPTION_KEY"] = key

 
load_dotenv(find_dotenv())
encryption_key = Fernet(os.getenv("ENCRYPTION_KEY"))



def inpAdd():
    rows = int(input("How many rows do you want to add? "))

    for i in range(rows):
        type = input("Enter the type of entry that you are saving(API, password, or note):  ")
        name = input("Enter the name of the entry:   ")
        value = encryption_key.encrypt(
            input("Enter the value of the entry: ").encode("utf-8")
        )

        if name in lsNames():
            print(f"ERROR: The database already contains {name}.")
            continue
        else:
            addRow(type, name, value)
        
def inpRemove():
    name = str(input("Witch row do you want to remove?  "))

    if name in lsNames():
        removeRow(name)
    else:
        print(f"ERROR: {name} is not in the database.")

def printTypes():
    print(" ")
    print("These are the types of entries you have:")
    cur.execute("""
        SELECT DISTINCT type FROM secrets;
    """)
    base = cur.fetchall()
    for row in base:
        print(list(str(value) for value in row))

def printDatabase():
    cur.execute("SELECT * FROM secrets ORDER BY type, name;")
    columns = [description[0] for description in cur.description]
    print(" | ".join(columns))
    print("-" * 50)

    for row in cur.fetchall():
        decrypted = encryption_key.decrypt(row[2]).decode('utf-8')
        new_tuple = [row[0], row[1], decrypted]
        print(" | ".join(str(value) for value in new_tuple))



def addRow(type, name, value):
    if type.lower() == "api" or type.lower() == "password" or type.lower() == "note":
        cur.execute("""
        INSERT INTO secrets VALUES
            (?, ?, ?)
        """, (name, type.lower(), value))
        con.commit()
    else:
        print("is invald.")

def removeRow(name):
    cur.execute("""
        DELETE FROM secrets
        WHERE name = ?
    """, (name,))
    con.commit()

def lsNames():
    cur.execute("""
            SELECT name FROM secrets;
        """)
        
    ls_name = [row[0] for row in cur.fetchall()]
    return ls_name


printDatabase()
printTypes()