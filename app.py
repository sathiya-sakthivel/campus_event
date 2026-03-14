
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        venue TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        event_name TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    conn.close()
    return render_template("index.html", events=events)


@app.route('/create_event', methods=['GET','POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        venue = request.form['venue']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events(name,date,venue) VALUES(?,?,?)",(name,date,venue))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("create_event.html")


@app.route('/register/<event_name>', methods=['GET','POST'])
def register(event_name):

    if request.method == 'POST':
        student = request.form['student']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registrations(student_name,event_name) VALUES(?,?)",(student,event_name))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("register_event.html", event_name=event_name)


if __name__ == '__main__':
    app.run(debug=True)
