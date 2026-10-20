import os
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, url_for

APP_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("TASKFLOW_DB", os.path.join(APP_DIR, "taskflow.db"))

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.get("/")
def index():
    with get_db() as conn:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    return render_template("index.html", tasks=tasks, total=total,
                           completed=completed, pending=total-completed)

@app.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    if title:
        with get_db() as conn:
            conn.execute("INSERT INTO tasks (title, description) VALUES (?, ?)",
                         (title, description))
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    with get_db() as conn:
        conn.execute("UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?",
                     (task_id,))
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))

@app.get("/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1").fetchone()
        return jsonify(status="ok", application="TaskFlow"), 200
    except sqlite3.Error:
        return jsonify(status="error", application="TaskFlow"), 500

@app.get("/api/tasks")
def api_tasks():
    with get_db() as conn:
        tasks = conn.execute("SELECT id, title, description, completed, created_at FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([dict(task) for task in tasks])

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
