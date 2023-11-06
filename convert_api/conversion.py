from flask import Flask, request, jsonify, send_file
import os
import uuid
import subprocess
from zipfile import ZipFile

app = Flask(__name__)

@app.route('/create_conversion_instance', methods=['POST'])
def create_conversion_instance():
    image_set = request.json['conjunto_imagens1']
    weights = request.json['peso_zip']


    unicode = str(uuid.uuid4())

    instance_folder = f"conversoes/{unicode}"
    os.mkdir(instance_folder)

    os.mkdir(instance_folder+"/testA/")
    for idx, base64_image in enumerate(image_set):
        with open(instance_folder + f"/images_to_convert/{idx}.png", "wb") as file:
            file.write(base64_image.decode('base64'))

    os.mkdir(instance_folder+"/weights/")
    with open(instance_folder + f"/weights/{idx}.zip", "wb") as file:
        file.write(weights.decode('base64'))
    
    with ZipFile(instance_folder+"/weights/pesos.zip", 'r') as zip_file:
        zip_file.extractall(instance_folder+"/weights/")


    os.mkdir(instance_folder+"/converted_images/")


    process = subprocess.Popen(["python3", "../cyclegan/convert.py", "--dataroot", instance_folder+"/testA", "--name", unicode, 
                                "--checkpoints_dir", instance_folder + "/weights", "--model", "test", "--no_dropout"
                                "--num_thread", "0", "--batch_size", "1", "--serial_batches", "--no_flip", 
                                "--results_dir", instance_folder + "/converted_images/"])

    id_do_processo=str(process.pid)

    token = f"{unicode}_{id_do_processo}"

    return jsonify({'codigo_instancia': token})