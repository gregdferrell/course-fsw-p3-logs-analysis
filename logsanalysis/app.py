from logsanalysis.db_init import conn

# Test DB conn
cursor = conn.cursor()
cursor.execute("SELECT * FROM authors")
rows = cursor.fetchall()
conn.close()
print(rows)
