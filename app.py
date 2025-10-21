from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from color_analyzer import analyze_dominant_color # Importa a função criada acima

app = Flask(__name__)

@app.route('/analyze_color', methods=['POST'])
def analyze_color():
    # Verifica se os dados necessários estão presentes na requisição
    if 'image_base64' not in request.json or 'target_color' not in request.json:
        return jsonify({
            "error": "Dados incompletos. Requer 'image_base64' e 'target_color'."
        }), 400

    try:
        # 1. Recupera os dados
        img_b64 = request.json['image_base64']
        target_color = request.json['target_color']
        
        # 2. Converte a string Base64 de volta para a imagem (array numpy)
        img_bytes = base64.b64decode(img_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Não foi possível decodificar a imagem."}), 400

        # 3. Analisa a cor usando a função do seu código
        is_correct = analyze_dominant_color(img, target_color)

        # 4. Retorna o resultado
        return jsonify({
            "target_color": target_color,
            "result": is_correct
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Execute a API em modo debug
    app.run(debug=True)