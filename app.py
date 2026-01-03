from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "tasks.db"

def get_db():
    return sqlite3.connect(DB_NAME)

@app.route("/")
def home():
    return render_template("index.html")

# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": t[0], "title": t[1], "completed": bool(t[2])}
        for t in tasks
    ])

# Add task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)",
                   (data["title"], 0))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added"})

# Update task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task updated"})

# Delete task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
