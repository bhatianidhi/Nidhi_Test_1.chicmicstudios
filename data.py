import mysql.connector
from mysql.connector import Error

try:
    # 1️⃣ Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # replace with your MySQL root password
        database="sab"        # replace with your database name
    )
    
    cursor = conn.cursor()
    print("Connected to MySQL!\n")

    # 2️⃣ Query all data from 'data' table
    query = "SELECT * FROM data"
    cursor.execute(query)
    rows = cursor.fetchall()

    # 3️⃣ Print the results
    if rows:
        print(f"Fetched {len(rows)} rows from 'data' table:\n")
        for row in rows:
            print(row)
    else:
        print("The table 'data' is empty.")

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    # 4️⃣ Close connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("\nConnection closed.")
