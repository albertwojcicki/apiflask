from flask import Flask, request, render_template
import sqlite3
import requests

app = Flask(__name__)


con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()

cur.execute(""" CREATE TABLE
            IF NOT EXISTS
            brukere(ID integer PRIMARY KEY, 
            navn text
            )""")

cur.execute(""" CREATE TABLE
            IF NOT EXISTS
            todo(ID integer PRIMARY KEY, 
            bruker_id integer,
            todo text
            )""")

brukere = ["Albert", "Mats"]

cur.executemany("INSERT INTO brukere (navn) VALUES (?)", [(bruker,) for bruker in brukere])
con.commit()

@app.route('/get_todos', methods = ["GET"])
def get_todos():
  id = request.get_json()["id"]
  cur.execute("SELECT todo.id, todo.todo FROM brukere INNER JOIN todo ON todo.bruker_id = brukere.id WHERE brukere.id = ?", (id,))
  data = cur.fetchall()
  content = []
  for todo in data:
    content.append({"id": todo[0], "todo": todo[1]})
  return content

@app.route("/logginn", methods=["GET"])
def logginn():
    navn = request.get_json()["navn"]
    cur.execute("SELECT id FROM brukere WHERE navn = ?", (navn,))
    result = cur.fetchone()
    if result:
        bruker_id = result[0]
        cur.execute("SELECT todo.id, todo.todo FROM brukere INNER JOIN todo ON todo.bruker_id = brukere.id WHERE brukere.id = ?", (bruker_id,))
        data = cur.fetchall()
        content = [{"id": todo[0], "todo": todo[1]} for todo in data]
        return {"Status": "A user", "id": bruker_id, "navn": navn, "todos": content}
    else:
        return {"Status": "Not a user"}


@app.route('/leggTilTodo', methods = ["POST"]) 
def leggTilTodo():
  todo = request.get_json()["todo"]
  id = request.get_json()["id"]
  cur.execute("INSERT INTO todo(id, todo) VALUES(?,?)", (id, todo))
  con.commit()
  return {"Status": "no error"}
    


if __name__ == "__main__":
    app.run(debug=True, port=5020)
