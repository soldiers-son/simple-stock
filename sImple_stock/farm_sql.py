import sqlite3

conn = sqlite3.connect('farm.db')
c = conn.cursor() 


#######################################
# Create Tables for application entries
#######################################

# c.execute("""CREATE TABLE IF NOT EXISTS users (
#     username TEXT PRIMARY KEY,
#     password_hash BLOB
# )""")

# c.execute("""CREATE TABLE IF NOT EXISTS plant (
#              type string,
#              amount float,
#              date DATE
#             )""")

# c.execute("""CREATE TABLE IF NOT EXISTS harvest (
#              type string,
#              amount string,
#              date DATE
#             )""")

# c.execute (""" CREATE TABLE IF NOT EXISTS task_complete (
#            name string,
#            date DATE,
#            task string
#            )""")

# c.execute (""" CREATE TABLE IF NOT EXISTS tools (
#            tool string,
#            quantity int
#            )""")

# c.execute (""" CREATE TABLE IF NOT EXISTS farm_supply (
#            item string,
#            quatity int,
#            date DATE
#            )""")

# c.execute (""" CREATE TABLE IF NOT EXISTS animal_supply (
#            item string,
#            quatity int,
#            price float,
#            date DATE 
#            )""")

#######################
# Basic sqlite3 commands
#######################

# c.execute("SELECT * FROM task_tracker WHERE name=''")
# print(c.fetchone())
# print(c.fetchall())
# print(c.fetchmany())

# c.execute("DELETE FROM task_tracker")

# c.execute ("SELECT * FROM harvest WHERE type = 'Tomatoes' ")
# print(c.fetchall())

conn.commit()
print('Data entry successful')
conn.close()
