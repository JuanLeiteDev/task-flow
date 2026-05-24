from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

import json

ESTADOS = ["Pendente", "Atrasada", "Concluída"]

app = Flask(__name__)

@app.route("/")
def home():
    tarefas = carregar_tarefas()
    tarefas_pendentes = [tarefa for tarefa in tarefas["tarefas"] if tarefa["estado"] == ESTADOS[0]]
    tarefas_atrasadas = [tarefa for tarefa in tarefas["tarefas"] if tarefa["estado"] == ESTADOS[1]]
    tarefas_concluidas = [tarefa for tarefa in tarefas["tarefas"] if tarefa["estado"] == ESTADOS[2]]
    return render_template(
        "listar.html", 
        tarefas_pendentes=tarefas_pendentes,
        tarefas_atrasadas=tarefas_atrasadas,
        tarefas_concluidas=tarefas_concluidas
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
    if(len(categorias) > 30): erros["categoria"] = "A categoria deve ter no máximo 30 caracteres."

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

    if not adicionar_tarefa(nova_tarefa):
        return render_template(
            "criar.html",
            erros="Erro ao guardar tarefa no arquivo JSON",
            dados=request.form
        ), 400
    return redirect(url_for('home'))

@app.route("/listar")
def listar():
    return redirect(url_for('home'))

@app.route("/apagar/<id_tarefa>", methods=["POST"])
def apagar(id_tarefa: int):
    tarefas_json = carregar_tarefas()
    tarefas: list[dict] = tarefas_json["tarefas"]

    if not any(int(tarefa["id"]) == int(id_tarefa) for tarefa in tarefas): return {"sucesso": False, "mensagem": "Tarefa não existe."}

    tarefas_json["tarefas"] = [tarefa for tarefa in tarefas if int(tarefa["id"]) != int(id_tarefa)]
    if salvar_tarefas(tarefas_json): return {"sucesso": True, "mensagem": "Tarefa apagada com sucesso!"}
    else: return {"sucesso": False, "mensagem": "Erro ao tentar apagar tarefa do banco."}

def carregar_tarefas() -> dict[list]:
    try:
        with open("tarefas.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {
            "ultimo-id-usado": 0,
            "categorias": [],
            "tarefas": []
        }
    
def salvar_tarefas(tarefas):
    try:
        with open("tarefas.json", "w") as file:
            json.dump(tarefas, file, indent=4, ensure_ascii=False)
            return True
    except Exception:
        return False
    
def adicionar_tarefa(nova: dict):
    tarefas = carregar_tarefas()

    nova["id"] = tarefas["ultimo-id-usado"] + 1
    tarefas["ultimo-id-usado"] += 1

    tarefas["tarefas"].append(nova)

    try:
        categoria = nova.get("categoria", "")
        categorias_existentes = tarefas["categorias"]
        if categoria not in categorias_existentes and categoria != "": tarefas["categorias"].append(categoria)
    except Exception:
        pass

    return salvar_tarefas(tarefas)

if __name__ == "__main__":
    app.run()