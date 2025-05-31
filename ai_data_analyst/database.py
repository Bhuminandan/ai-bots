import sqlite3

# Create database
connection = sqlite3.connect("student.db")

# Create cursor
cursor = connection.cursor()

# Create table query 
create_table_query = """
CREATE TABLE IF NOT EXISTS STUDENT (
   NAME VARCHAR(25),
   COURSE VARCHAR(25),
   SECTION VARCHAR(25),
   MARKS INT
)
"""

cursor.execute(create_table_query)

# Insert records
sql_query="""
INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS) VALUES (?, ?, ?, ?)
"""
values = [
   ('Student 1', 'Data science', 'A', 90),
   ('Student 2', 'Data science', 'B', 100),
   ('Student 3', 'Data science', 'A', 86),
   ('Student 4', 'DEVOPS', 'A', 30),
   ('Student 5', 'DEVOPS', 'A', 70),
]

cursor.executemany(sql_query, values)
connection.commit()