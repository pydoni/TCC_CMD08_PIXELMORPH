from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/create_train_instance', methods=['POST'])
def create_conversion_instance():
    image_set_a = request.json['conjunto_imagens1']
    image_set_b = request.json['conjunto_imagens2']

    unicode = str(uuid.uuid4())

    instance_folder = f"treinamentos/{unicode}"
    os.mkdir(instance_folder)

    os.mkdir(instance_folder+"/trainA/")
    for idx, base64_image in enumerate(image_set_a):
        with open(instance_folder + f"/trainA/{idx}.png", "wb") as file:
            file.write(base64_image.decode('base64'))

    os.mkdir(instance_folder+"/trainB/")
    for idx, base64_image in enumerate(image_set_b):
        with open(instance_folder + f"/trainB/{idx}.png", "wb") as file:
            file.write(base64_image.decode('base64'))
    
    process = subprocess.Popen(["python3", "../cyclegan/train.py", "--dataroot", instance_folder, "--name", unicode, 
                                "--checkpoints_dir", instance_folder, "--model", "cycle_gan"])

    id_do_processo=str(process.pid)

    token = f"{unicode}_{id_do_processo}"

    return jsonify({'codigo_instancia': token})