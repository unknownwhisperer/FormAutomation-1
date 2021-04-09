import sqlite3  
  
con = sqlite3.connect("database.db")  
print("Database opened successfully")  
  
con.close()  