from flask import Flask, request, jsonify
import sqlite3
from PIL import Image
import torch
import io
import numpy as np
from datetime import datetime


app = Flask(__name__)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./src/best.pt')

def conectar_bd():
    conn = sqlite3.connect('./database/database.db')
    return conn

def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS predicoes (code TEXT, value TEXT, date TEXT)')
    conn.commit()
    conn.close()

criar_tabela()

def getDate():
    date = datetime.now()
    return date.strftime('%Y-%m-%d')

@app.route('/enviar_imagem', methods=['POST'])
def enviar_imagem():
    try:
        codigo = request.headers.get('codigo')  # Pega o código do cabeçalho da requisição
        imagem = request.data  # Pega a imagem do corpo da requisição

        print(codigo)

        imagem_pil = Image.open(io.BytesIO(imagem))
        imagem_pil.save("temp.jpg")
        imagem_numpy = np.array(imagem_pil)
        
        results = model(imagem_numpy)
        my_number = ''

        # Ordenar as caixas delimitadoras da direita para a esquerda
        bboxes = results.pandas().xyxy[0].sort_values(by='xmin', ascending=False)

        # Extrair ROIs contidas nas bounding boxes
        for _, pred in bboxes.iterrows():
            # xmin, ymin, xmax, ymax = pred[:4]  # Extrair apenas as coordenadas (xmin, ymin, xmax, ymax)
            label = pred['name']  # Extrair o rótulo previsto

            my_number += label

        my_number = my_number[::-1]

        print(f'\n\nO número no display é {my_number}\n\n')

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO predicoes (code, value, date) VALUES (?, ?, ?)', (codigo, my_number, getDate()))
        conn.commit()
        conn.close()

        return jsonify({"mensagem": f'Predição {my_number} salva com sucesso.'})

    except Exception as e:
        return jsonify({"erro": str(e)})
    
@app.route('/valores_recentes', methods=['GET'])
def valores_recentes():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('SELECT code, value, date FROM predicoes ORDER BY code DESC LIMIT 10')
        resultados = cursor.fetchall()
        conn.close()

        valores = [{"code": row[0], "value": row[1], "date": row[2]} for row in resultados]

        return jsonify(valores)

    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

