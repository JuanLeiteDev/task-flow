from flask import Flask, request, render_template
from datetime import datetime

import json

app = Flask(__name__)

@app.route("/")
def home():
    tarefas = carregar_tarefas()
    return render_template(
        "listar.html", 
        tarefas=tarefas
    )

@app.route("/criar")
def criar():
    return render_template("criar.html")

@app.route("/listar")
def listar():
    tarefas = carregar_tarefas()
    return render_template("listar.html", tarefas=tarefas)

def carregar_tarefas():
    caminho = "tarefas.json"
    with open(caminho, "r") as file:
        tarefas = json.load(file)
        return tarefas
    

if __name__ == "__main__":
    app.run()