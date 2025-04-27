from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import os

app = FastAPI()

# Database connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "testdb")

class Item(BaseModel):
    name: str
    description: str = None

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.post("/items")
def insert_item(item: Item):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s)",
            (item.name, item.description)
        )
        connection.commit()
        cursor.close()
        return {"message": "Item inserted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error inserting item: {e}")
    finally:
        if connection.is_connected():
            connection.close()

@app.get("/items")
def read_items():
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        cursor.close()
        return {"items": rows}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error reading items: {e}")
    finally:
        if connection.is_connected():
            connection.close()
