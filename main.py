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

    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "API çalışıyor"}

# 🔹 TÜM SÜREÇLERİ GETİR
@app.get("/processes")
def get_processes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, process_name FROM processes ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"id": r[0], "process_name": r[1]} for r in rows]

# 🔹 SÜREÇ EKLE
@app.post("/processes")
def add_process(payload: dict):
    name = payload.get("process_name")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO processes (process_name) VALUES (%s) RETURNING id, process_name",
        (name,)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {"id": row[0], "process_name": row[1]}

# 🔹 SÜREÇ GÜNCELLE
@app.put("/processes/{process_id}")
def update_process(process_id: int, payload: dict):
    name = payload.get("process_name")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE processes SET process_name=%s WHERE id=%s RETURNING id, process_name",
        (name, process_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {"id": row[0], "process_name": row[1]}

# 🔹 SÜREÇ SİL
@app.delete("/processes/{process_id}")
def delete_process(process_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM processes WHERE id=%s", (process_id,))
    conn.commit()
    cur.close()
    conn.close()

    return {"status": "deleted"}
