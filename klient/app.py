import json
from flask import Flask, request, render_template, json, redirect, url_for
import requests


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logginn", methods=["GET", "POST"])
def logginn():
    if request.method == "POST":
        navn = request.form.get("navn")
        data = {"navn": navn}
        response = requests.get('http://127.0.0.1:5020/logginn', json=data)
        try:
            content = response.json()
        except ValueError:
            return render_template("index.html", feil="Ugyldig respons fra serveren")

        if content.get("Status") == "A user":
           
            return render_template('todo_page.html', data=data)
        else:
            return render_template("index.html", feil="Feil brukernavn")

@app.route("/leggTilTodo/<id>", methods = ["POST"])
def todo_post(id):
  todo = request.form.get("todo")
  requests.post('http://127.0.0.1:5020/leggTilTodo', json={"id": id, "todo": todo})
  return redirect(url_for('todo_page', id=id))

@app.route("/todo_page/<id>", methods = ["GET"])
def home_page(id):
  data = requests.get('http://127.0.0.1:5020/get_todos', json={"id": id}).json()
  return render_template("todo_page.html", id=id, data=data)
    
if __name__ == "__main__":
    app.run(debug=True, port=5010)
