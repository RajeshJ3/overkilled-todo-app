from os import environ as env

BOUNDED_CONTEXT_NAME = "accounts_context"

DB_HOST = env.get("DB_HOST", f"{BOUNDED_CONTEXT_NAME}_db")
DB_PORT = env.get("DB_PORT", "5432")
DB_USER = env.get("DB_USER")
DB_PASSWORD = env.get("DB_PASSWORD")
DB_NAME = env.get("DB_NAME")
