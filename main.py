from fastapi import FastAPI,Form
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app=FastAPI()
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="test"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/get_email")
async def get_email(mail:str=Form(...)):  
    cursor=conn.cursor()
    cursor.execute("select * from customer where CSTM_EMAIL=(%s)",(mail,))
    records=cursor.fetchone()
    if records==None:
        return "please enter valid email id"
    else:
        return "email id found"