from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS processes (
        id SERIAL PRIMARY KEY,
        process_name VARCHAR(150) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        ad_soyad VARCHAR(150),
        sicil_no VARCHAR(50),
        pozisyon VARCHAR(100),
        departman VARCHAR(100)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "API çalışıyor"}