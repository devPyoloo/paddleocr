from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS
from PIL import Image
import numpy as np
import json

app = Flask(__name__)
CORS(app)

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_boxes_and_text(results):
    extracted_data = []
    if not results:
        return extracted_data

    for result in results:
        for line in result:
            if len(line) >= 2 and isinstance(line[1], (tuple, list)):
                box = line[0]  # 🔹 Coordinates (Remove this)
                text_info = line[1]
                if len(text_info) >= 1 and isinstance(text_info[0], str):
                    text = text_info[0]
                    extracted_data.append({"text": text}) 
            else:
                print(f"Skipping invalid line: {line}")
    return extracted_data


def process_image(image, regions):
    """Extract text from predefined regions in the image."""
    text_data = []
    
    for region in regions:
        x, y, width, height = region['x'], region['y'], region['width'], region['height']
        cropped_image = image.crop((x, y, x + width, y + height))
        cropped_image_np = np.array(cropped_image)
        
        result = ocr.ocr(cropped_image_np, cls=True)
        print(f"OCR Result: {result}")

        if result:
            ocr_text_data = extract_boxes_and_text(result)  # Already modified to remove boxes
            text_data.extend(ocr_text_data)
        else:
            text_data.append({"text": "No text detected in this region"})
    
    return text_data


@app.route('/extract-text/simple', methods=['POST'])
def extract_text_simple():
    try:
        print(f"Received form data: {request.form}")
        print(f"Received files: {request.files}")

        if 'file' not in request.files:
            return jsonify({"error": "Missing file parameter"}), 400
        if 'regions' not in request.form:
            return jsonify({"error": "Missing regions parameter"}), 400

        file = request.files['file']
        regions = json.loads(request.form['regions'])  # Parse regions
        
        image = Image.open(file.stream)
        text_data = process_image(image, regions)
        image.close()

        return jsonify({
            "message": "Text extraction successful",
            "data": text_data
        })

    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='localhost', port=5002, debug=True)
