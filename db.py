import pyodbc
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def get_connection():
    cfg = load_config()
    conn_str = (
        f"DRIVER={{{cfg['driver']}}};"
        f"SERVER={cfg['server']};"
        f"DATABASE={cfg['database']};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)