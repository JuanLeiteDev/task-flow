from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

import json

ESTADOS = ["Pendente", "Atrasada", "Concluída"]

app = Flask(__name__)

@app.route("/")
def home():
    tarefas = carregar_tarefas()
    return render_template(
        "listar.html", 
        tarefas=tarefas
    )

@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "GET":
        return render_template("criar.html", erros={}, dados={})
    
    erros = {}

    titulo = request.form.get('titulo', "").strip()
    if not titulo: erros["titulo"] = "O título é obrigatório."
    if len(titulo) > 20: erros["titulo"] = "O título deve ter no máximo 20 caracteres."

    descricao = request.form.get('desc', "").strip()
    if len(descricao) > 200: erros["descricao"] = "O tamanho máximo da descrição é de 200 caracteres."

    categorias = request.form.get('cat', "").strip()

    estado = request.form.get('status', "").strip()
    if estado not in ESTADOS: erros["estado"] = f"O estados disponíveis são: {ESTADOS[0]}, {ESTADOS[1]} e {ESTADOS[2]}"

    data_limite = request.form.get('limite', "").strip()
    if not data_limite: data_limite = "Sem data limite"
    else: 
        try:
            data_limite = datetime.strptime(data_limite.strip(), "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception:
            erros["data"] = "Data inválida."

    if erros:
        return render_template(
            "criar.html",
            erros=erros,
            dados=request.form
        ), 400

    data_inicio = datetime.today().strftime("%d/%m/%Y")

    nova_tarefa = {
        "titulo": titulo[:20],
        "descricao": descricao[:200],
        "categoria": categorias.capitalize(),
        "inicio": data_inicio,
        "fim": data_limite,
        "estado": estado,
    }

    adicionar_tarefa(nova_tarefa)
    return redirect(url_for('home'))

@app.route("/listar")
def listar():
    tarefas = carregar_tarefas()
    return render_template("listar.html", tarefas=tarefas)

def carregar_tarefas() -> dict[list]:
    caminho = "tarefas.json"
    with open(caminho, "r") as file:
        tarefas = json.load(file)
        return tarefas
    
def adicionar_tarefa(nova: dict):
    tarefas = carregar_tarefas()

    match nova['estado']:
        case "Pendente":
            tarefas['pendentes'].append(nova)
        case "Atrasada":
            tarefas['atrasadas'].append(nova)
        case "Concluída":
            tarefas['concluidas'].append(nova)

    try:
        categoria = nova.get("categoria", "")
        categorias_existentes = tarefas["categorias"]
        if categoria not in categorias_existentes and categoria != "": tarefas["categorias"].append(categoria)
    except Exception:
        pass

    with open("tarefas.json", "w") as file:
        json.dump(tarefas, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    app.run()