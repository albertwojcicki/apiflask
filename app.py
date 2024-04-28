from flask import Flask, request, render_template, jsonify
import sqlite3

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

brukere = ["Albert", "Mats", "Kjell"]
cur.execute("DELETE FROM brukere")
con.commit()
cur.executemany("INSERT INTO brukere (navn) VALUES (?)", [(bruker,) for bruker in brukere])
con.commit()

@app.route('/get_todos', methods = ["GET"])
def get_todos():
  id = request.get_json()["id"]
  cur.execute("SELECT todo.ID, todo.todo FROM brukere JOIN todo ON todo.bruker_id = brukere.ID WHERE brukere.ID = ?", (id,))
  data = cur.fetchall()
  content = []
  for todo in data:
    print(todo)
    content.append({"todoId": todo[0], "todo": todo[1]})
  return content

@app.route("/logginn", methods=["POST"])
def logginn():
    if request.is_json:
        navn = request.json.get("navn")
        cur.execute("SELECT ID FROM brukere WHERE navn = ?", (navn,))
        result = cur.fetchone()
        
        if result:
            cur.execute("SELECT ID FROM todo")
            todo_ids = [row[0] for row in cur.fetchall()]
            return jsonify({"Status": "A user", "id": result[0], "navn": navn, "todo_ids": todo_ids})
        else: 
            return jsonify({"Status": "Not a user"}), 404
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415


@app.route('/leggTilTodo', methods = ["POST"]) 
def leggTilTodo():
  todo = request.get_json()["todo"]
  id = request.get_json()["id"]
  cur.execute("INSERT INTO todo(bruker_id, todo) VALUES(?,?)", (id, todo))
  con.commit()
  return {"Status": "no error"}
    

@app.route('/endreTodo', methods=["GET", "PUT"])
def endreTodo():
  if request.method == "GET":
    id = request.get_json()["id"]
    cur.execute("SELECT todo.ID, todo.todo FROM brukere INNER JOIN todo ON todo.bruker_id = brukere.ID WHERE todo.ID = ?", (id,))
    data = cur.fetchone()
    content = {"id": data[0], "todo": data[1]}
    return content
  
  if request.method == "PUT":
    id = request.get_json()["id"]
    todo = request.get_json()["todo"]
    cur.execute("UPDATE todo SET todo = ? WHERE ID=?", (todo, id))
    con.commit()
    return {"Status": "no error"}
     
   
@app.route('/slettTodo', methods=["POST"])
def slettTodo():
    data = request.get_json()
    id = data["id"]
    todoId = data["todoId"]
    cur.execute("DELETE FROM todo WHERE bruker_id=? AND ID=?", (id, todoId))
    con.commit()
    return {"Status": "no error"}




if __name__ == "__main__":
    app.run(debug=True, port=5020)