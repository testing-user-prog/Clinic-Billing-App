import pyodbc
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def get_connection():
    cfg = load_config()
    if cfg['trusted_connection']:
        conn_str = (
            f"DRIVER={{{cfg['driver']}}};"
            f"SERVER={cfg['server']};"
            f"DATABASE={cfg['database']};"
            f"Trusted_Connection=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{{cfg['driver']}}};"
            f"SERVER={cfg['server']};"
            f"DATABASE={cfg['database']};"
            f"UID={cfg['username']};"
            f"PWD={cfg['password']};"
        )
    return pyodbc.connect(conn_str)