from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

username = 'root'
password = ''
host = 'localhost'
database = 'json'

cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    database=database
)

cursor = cnx.cursor()

class Userschema(BaseModel):
    id: int
    fullName: str
    email: str
    password: str

@app.get("/users/")
async def get_user_by_email(email: str):
    try:
        logging.info(f"Received request for user with email {email}")
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        if user is None:
            logging.info(f"User with email {email} not found")
            raise HTTPException(status_code=404, detail="User not found")
        return [
            {
                "fullName": user[1],
                "email": user[2],
                "password": user[3],
                "id": str(user[0])
            }
        ]
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

class User(BaseModel):
    id: int = None
    fullName: str
    email: str
    password: str

@app.post("/users/")
async def create_user(user: User):
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (user.fullName, user.email, user.password))

    cnx.commit()
    return {"message": "User created successfully"}
        
