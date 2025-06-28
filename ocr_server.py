from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import re

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    try:
        image = Image.open(file.stream)
        text = pytesseract.image_to_string(image)

        codes = re.findall(r'\b\d{10,18}\b', text)

        return jsonify({'recharge_codes': codes, 'raw_text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
