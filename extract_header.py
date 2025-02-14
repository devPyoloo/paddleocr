from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS
from PIL import Image
import numpy as np
import os
import json

app = Flask(__name__)
CORS(app)

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_header(image):
    """Extract text from the top 20% of the image (header section)."""
    image_width, image_height = image.size
    header_height = int(image_height * 0.20)  # Define top 20% as header

    # Crop the header section
    header_image = image.crop((0, 0, image_width, header_height))
    header_np = np.array(header_image)

    # Run OCR on the header
    result = ocr.ocr(header_np, cls=True)
    
    # Extract only the text
    extracted_text = [line[1][0] for line in result[0] if len(line) > 1 and line[1]]

    return extracted_text


@app.route('/extract-header', methods=['POST'])
def extract_header_text():
    try:
        file = request.files['file']
        image = Image.open(file.stream)

        header_text = extract_header(image)
        image.close()

        return jsonify({
            "message": "Header extraction successful",
            "data": header_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)
