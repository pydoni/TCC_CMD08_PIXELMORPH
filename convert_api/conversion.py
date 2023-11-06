from flask import Flask, request, jsonify, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

@app.route('/create_conversion_instance', methods=['POST'])
def create_conversion_instance():
    conjunto_imagens1 = request.json['conjunto_imagens1']
    peso_zip = request.json['peso_zip']

    codigo_unico = str(uuid.uuid4())

    os.mkdir(f"instancias_de_treino/{codigo_unico}")
    # python3 convert.py --dataroot datasets/horse2zebra/testA --checkpoints_dir conversao --name 1111 --model test
    #  --no_dropout --num_thread 0 --batch_size 1 --serial_batches --no_flip --results_dir conversao/2104194/
    process = subprocess.Popen(["python3", "../cyclegan/test.py", "--dataroot", f"../instancias_de_conversão/{codigo_unico}/testA"
                                "--name ", "", "--model", "test", "--no_dropout"])

    id_do_processo=str(process.pid)

    token = f"{codigo_unico}_{id_do_processo}"

    return jsonify({'codigo_instancia': token})