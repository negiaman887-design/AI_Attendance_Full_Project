from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("attendance.db")

conn=db()
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY, student_id TEXT UNIQUE, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY, student_id TEXT, date TEXT, time TEXT)")
conn.commit()
conn.close()

@app.route("/")
def home():
    conn=db()
    students=conn.execute("SELECT student_id,name FROM students").fetchall()
    attendance=conn.execute("SELECT student_id,date,time FROM attendance ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html",students=students,attendance=attendance)

@app.route("/register",methods=["POST"])
def register():
    sid=request.form["student_id"]
    name=request.form["name"]
    conn=db()
    conn.execute("INSERT OR IGNORE INTO students(student_id,name) VALUES(?,?)",(sid,name))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
