import json
import mysql.connector

with open('db.json') as f:
    data = json.load(f)

users = data.get('users')

cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='json'
)
next_id = 1
for user in users:
    user["id"]=next_id
    next_id=next_id+1

cursor = cnx.cursor()
for user in users:
    query = "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user.get('id'), user.get('fullName'), user.get('email'), user.get('password')))

cnx.commit()

cursor.close()
cnx.close()