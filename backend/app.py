# from lines 3 to 48, I asked chatGPT how to write a flask application that connects to a MySQL database, provides a health check endpoint, a database test endpoint, and an endpoint to initialize the database using a schema.sql file. 

from flask import Flask, jsonify # 
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

@app.get("/health")
def health():
    return jsonify({"status": "server running"})


@app.get("/db-test")
def db_test():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS test")
            result = cur.fetchone()

        return jsonify({"database": "connected", "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/init-db")
def init_db():
    try:
        conn = get_connection()

        with open("schema.sql") as f:
            schema = f.read()

        with conn.cursor() as cur:
            for statement in schema.split(";"):
                if statement.strip():
                    cur.execute(statement)

        return jsonify({"message": "Database initialized"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)