import json
from flask import Flask, request, render_template, json, redirect, url_for
import requests


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logginn", methods=["POST"])
def logginn():
    if request.method == "POST":
        navn = request.form.get("navn")
        data = {"navn": navn}
        response = requests.post('http://127.0.0.1:5020/logginn', json=data)
        try:
            content = response.json()
            
        except ValueError:
            return render_template("index.html", feil="Ugyldig respons fra serveren")
        
        if content.get("Status") == "A user":
            return redirect(url_for('todo_page', data=content["navn"], id=content["id"], todo_id=content["todo_ids"]))
        else:
            return render_template("index.html", feil="Feil brukernavn")

@app.route("/leggTilTodo/<id>", methods = ["POST"])
def leggTilTodo(id):
  todo = request.form.get("todoText")
  requests.post('http://127.0.0.1:5020/leggTilTodo', json={"id": id, "todo": todo})
  return redirect(url_for('todo_page', id=id))


@app.route("/todo_page/<id>", methods = ["GET"])
def todo_page(id):
  data = requests.get('http://127.0.0.1:5020/get_todos', json={"id": id}).json()
  print(data)
  return render_template("todo_page.html", id=id, data=data)


@app.route('/endreTodo/<id>/<todoId>', methods = ["GET", "POST"])
def endreTodo(id, todoId):
  if request.method == "GET":
    data = requests.get('http://127.0.0.1:5020/endreTodo', json={"id": todoId}).json()
    return render_template('endreTodo.html', id=id, todoId=data["id"], todo=data["todo"])
  
  if request.method == "POST":
    todo = request.form.get("todo")
    requests.put('http://127.0.0.1:5020/endreTodo', json={"id": todoId, "todo": todo})
    return redirect(url_for('todo_page', id=id))




@app.route("/slettTodo/<id>/<todoId>", methods=["POST"])
def slettTodo(id, todoId):
    requests.post('http://127.0.0.1:5020/slettTodo', json={"id": id, "todoId": todoId})
    return redirect(url_for('todo_page', id=id))



if __name__ == "__main__":
    app.run(debug=True, port=5010)