#1. from lines 3 to 48, I asked chatGPT how to write a flask application that connects to a MySQL database, provides a health check endpoint, a database test endpoint, and an endpoint to initialize the database using a schema.sql file. 

from flask import Flask, jsonify #1. PT.1               START
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
        return jsonify({"error": str(e)}), 500 #1. PT.1             END


#2. From lines 49 to 128, I asked chatGPT how to write Flask endpoints for CRUD operations on a "member" resource that will interact with a MySQL database using the get_connection function. 
from flask import request

@app.get("/members")
def get_members():
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM member")
        members = cur.fetchall()

    return jsonify(members)

@app.get("/members/<int:member_id>")
def get_member(member_id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM member WHERE id = %s", (member_id,))
        member = cur.fetchone()

    if not member:
        return jsonify({"error": "Member not found"}), 404

    return jsonify(member)

@app.post("/members")
def create_member():
    data = request.json

    name = data.get("name")
    details = data.get("details")
    title = data.get("title")
    level = data.get("level")

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO member (name, details, title, level)
            VALUES (%s, %s, %s, %s)
            """,
            (name, details, title, level),
        )

        member_id = cur.lastrowid

    return jsonify({"message": "Member created", "id": member_id}), 201

@app.put("/members/<int:member_id>")
def update_member(member_id):
    data = request.json

    name = data.get("name")
    details = data.get("details")
    title = data.get("title")
    level = data.get("level")

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE member
            SET name=%s, details=%s, title=%s, level=%s
            WHERE id=%s
            """,
            (name, details, title, level, member_id),
        )

    return jsonify({"message": "Member updated"})

@app.delete("/members/<int:member_id>")
def delete_member(member_id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("DELETE FROM member WHERE id=%s", (member_id,))

    return jsonify({"message": "Member deleted"}) #2. PT.2          END

# 3. From lines 131 to 216, I asked chatGPT how to write Flask endpoints for CRUD operations on an "event" resource that will interact with a MySQL database using the get_connection function.
@app.get("/events") # 3.       START
def get_events():
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM event")
        events = cur.fetchall()

    return jsonify(events)


@app.get("/events/<int:event_id>")
def get_event(event_id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM event WHERE id = %s", (event_id,))
        event = cur.fetchone()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify(event)


@app.post("/events")
def create_event():
    data = request.json

    name = data.get("name")
    capacity = data.get("capacity")
    level = data.get("level")
    date = data.get("date")

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO event (name, capacity, level, date)
                VALUES (%s, %s, %s, %s)
                """,
                (name, capacity, level, date),
            )

            event_id = cur.lastrowid

        return jsonify({"message": "Event created", "id": event_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.put("/events/<int:event_id>")
def update_event(event_id):
    data = request.json

    name = data.get("name")
    capacity = data.get("capacity")
    level = data.get("level")
    date = data.get("date")

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE event
            SET name=%s, capacity=%s, level=%s, date=%s
            WHERE id=%s
            """,
            (name, capacity, level, date, event_id),
        )

    return jsonify({"message": "Event updated"})


@app.delete("/events/<int:event_id>")
def delete_event(event_id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("DELETE FROM event WHERE id=%s", (event_id,))

    return jsonify({"message": "Event deleted"}) # 3.           END

if __name__ == "__main__": #1. PT 2 START
    app.run(debug=True) # 1.   PT.2   END.    