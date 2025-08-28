import psycopg2

# Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",            # change if needed
    password="1234",   # change to your actual password
    host="localhost",
    port="5432"
)

# Enable autocommit to allow CREATE DATABASE
conn.autocommit = True

# Create a cursor and execute SQL
cur = conn.cursor()
cur.execute("CREATE DATABASE project_db;")

# Clean up
cur.close()
conn.close()

print("Database 'project_db' created.")
