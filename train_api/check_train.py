from flask import Flask, request, jsonify, send_file
import psutil

app = Flask(__name__)

@app.route('/check_train_instance', methods=['GET'])
def check_train_instance():

    token = request.args.get('codigo_instancia')
    
    id_do_processo = token.split("_")[0]
    codigo_unico = token.split("_")[1]

    if psutil.pid_exists(id_do_processo):
        return jsonify({'status': "Treinamento em andamento"})
    else:
        arquivo_pesos = f"instancias_de_treino/{codigo_unico}/pesos.zip"
        return send_file(arquivo_pesos, as_attachment=True)

    

    