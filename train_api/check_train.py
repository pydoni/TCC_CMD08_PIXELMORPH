from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

@app.route('/check_train_instance', methods=['GET'])
def check_train_instance():

    token = request.args.get('codigo_instancia')
    
    codigo_unico = token.split("_")[1]
    arquivo_pesos = f"../treinamentos/{codigo_unico}/pesos.zip"

    if os.path.isfile(arquivo_pesos):
        return jsonify({'status': "Treinamento em andamento"})
    else:
        return send_file(arquivo_pesos, as_attachment=True)

    

    