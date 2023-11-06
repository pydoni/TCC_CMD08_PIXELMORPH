from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

@app.route('/check_conversion_instance', methods=['GET'])
def check_conversion_instance():
    token = request.args.get('codigo_instancia')
    
    codigo_unico = token.split("_")[1]
    arquivo_imagens = f"../conversaoes/{codigo_unico}/imagens.zip"

    if os.path.isfile(arquivo_imagens):
        return jsonify({'status': "Conversão em andamento"})
    else:
        return send_file(arquivo_imagens, as_attachment=True)