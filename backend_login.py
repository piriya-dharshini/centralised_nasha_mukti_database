import mysql.connector

def authenticate(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pdk164@#",
        database="NashaMukti"
    )
    cursor = mydb.cursor()

    query = "SELECT * FROM login WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        return user[0],user[3]  # Return the id and status of the authenticated user
    else:
        return None, None