from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    conn = get_conn()
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

@app.get("/processes")
def get_processes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, process_name FROM processes ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"id": row[0], "process_name": row[1]}
        for row in rows
    ]

@app.post("/processes")
def add_process(payload: dict):
    process_name = payload.get("process_name")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO processes (process_name) VALUES (%s) RETURNING id, process_name",
        (process_name,)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {"id": row[0], "process_name": row[1]}
