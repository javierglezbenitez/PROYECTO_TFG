import sqlite3
import os
import time
from src.LLM.src.config import DB_PATH


def resolve_db_path():
    if not DB_PATH or DB_PATH.strip() == "":
        base_folder = os.path.join("datos", "LLM", "User_DB")
        os.makedirs(base_folder, exist_ok=True)
        return os.path.join(base_folder, "user_data.db")
    return DB_PATH if DB_PATH.endswith(".db") else os.path.join(DB_PATH, "user_data.db")


DB_FILE = resolve_db_path()


def ensure_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS local_users (
        user_id TEXT,
        nombre TEXT,
        isla_residencia TEXT,
        municipio_residencia TEXT,
        ambiente TEXT DEFAULT 'estandar',
        nivel_intencion INTEGER,
        municipio_recomendado TEXT,
        alternativa_1 TEXT,
        alternativa_2 TEXT,
        fecha_consulta TEXT,
        tiempo_respuesta_ms REAL,
        PRIMARY KEY (user_id, nombre)
    );

    CREATE TABLE IF NOT EXISTS tourist_users (
        user_id TEXT,
        nombre TEXT,
        lugar_origen TEXT,
        isla_destino TEXT,
        ambiente TEXT DEFAULT 'estandar',
        nivel_intencion INTEGER,
        municipio_recomendado TEXT,
        alternativa_1 TEXT,
        alternativa_2 TEXT,
        fecha_consulta TEXT,
        tiempo_respuesta_ms REAL,
        PRIMARY KEY (user_id, nombre)
    );
    """)
    conn.commit()
    conn.close()
    print(f"[DB] Base de datos lista con soporte para ambientes en: {DB_FILE}")


def get_conn():
    conn = sqlite3.connect(DB_FILE,timeout=20)
    conn.row_factory = sqlite3.Row
    return conn

def save_full_intent(user_id, nombre, intent_dict):
    with get_conn() as conn:
        cur = conn.cursor()
        es_local = intent_dict.get("is_local", False)
        table = "local_users" if es_local else "tourist_users"

        create_empty_user(user_id, "local" if es_local else "turista", nombre=nombre)

        updates = []
        params = []

        campos = [
            "ambiente", "nivel_intencion", "municipio_recomendado",
            "alternativa_1", "alternativa_2", "fecha_consulta", "tiempo_respuesta_ms"
        ]

        for field in campos:
            if field in intent_dict and intent_dict[field] is not None:
                updates.append(f"{field} = ?")
                params.append(intent_dict[field])

        if es_local:
            if intent_dict.get("island"):
                updates.append("isla_residencia = ?")
                params.append(intent_dict["island"])
            if intent_dict.get("municipio"):
                updates.append("municipio_residencia = ?")
                params.append(intent_dict["municipio"])
        else:
            if intent_dict.get("island"):
                updates.append("isla_destino = ?")
                params.append(intent_dict["island"])
            if intent_dict.get("origin_city"):
                updates.append("lugar_origen = ?")
                params.append(intent_dict["origin_city"])

        if updates:
            sql = f"UPDATE {table} SET {', '.join(updates)} WHERE user_id = ? AND nombre = ?"
            params.extend([user_id, nombre])
            cur.execute(sql, params)
            conn.commit()

def create_empty_user(user_id, tipo, nombre=None, ambiente_detectado='estandar'):
    with get_conn() as conn:
        cursor = conn.cursor()
        table = "local_users" if tipo == "local" else "tourist_users"
        nombre_final = nombre if nombre else f"Anonimo_{int(time.time())}"

        query = f"INSERT OR IGNORE INTO {table} (user_id, nombre, ambiente) VALUES (?, ?, ?)"
        cursor.execute(query, (user_id, nombre_final, ambiente_detectado))
        conn.commit()
        return nombre_final


def get_user_profile(user_id, nombre=None):
    conn = get_conn()
    c = conn.cursor()

    for table in ["local_users", "tourist_users"]:
        if nombre:
            c.execute(f"SELECT * FROM {table} WHERE user_id=? AND nombre=?", (user_id, nombre))
        else:
            c.execute(f"SELECT * FROM {table} WHERE user_id=? ORDER BY ROWID DESC LIMIT 1", (user_id,))

        row = c.fetchone()
        if row:
            res = {"tipo": "local" if table == "local_users" else "turista", "data": dict(row)}
            conn.close()
            return res

    conn.close()
    return {"tipo": None, "data": {}}


def reset_user_data(user_id: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM local_users WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM tourist_users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()