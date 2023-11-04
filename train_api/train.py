from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/create_train_instance', methods=['POST'])
def create_conversion_instance():
    conjunto_imagens1 = request.json['conjunto_imagens1']
    conjunto_imagens2 = request.json['conjunto_imagens2']
    numero_epocas = request.json['numero_epocas']

    codigo_unico = str(uuid.uuid4())

    os.mkdir(f"instancias_de_treino/{codigo_unico}")

    process = subprocess.Popen(["python3", "hello"])

    id_do_processo=str(process.pid)

    token = f"{codigo_unico}_{id_do_processo}"

    return jsonify({'codigo_instancia': token})