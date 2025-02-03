from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Initialize OCR ---
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# --- Ensure Uploads Directory Exists ---
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Utility Functions ---
def extract_boxes_and_text(results):
    """Extract box coordinates and text from OCR results."""
    extracted_data = []
    if not results:
        return extracted_data
    
    for result in results:
        for line in result:
            if len(line) >= 2 and isinstance(line[1], (tuple, list)):
                box = line[0]  # Coordinates
                text_info = line[1]
                if len(text_info) >= 1 and isinstance(text_info[0], str):
                    text = text_info[0]
                    extracted_data.append({"box": box, "text": text})
            else:
                print(f"Skipping invalid line: {line}")
    return extracted_data


def scale_region(region, image_width, image_height, original_width, original_height):
    """Scale region coordinates to match image dimensions."""
    scaling_factor_x = image_width / original_width
    scaling_factor_y = image_height / original_height

    return {
        'x': region['x'] * scaling_factor_x,
        'y': region['y'] * scaling_factor_y,
        'width': region['width'] * scaling_factor_x,
        'height': region['height'] * scaling_factor_y,
    }


def process_image(image, regions, original_width, original_height):
    """Process image or image regions and extract text."""
    text_data = []
    for region in regions:
        scaled_region = scale_region(region, image.width, image.height, original_width, original_height)

        cropped_image = image.crop((
            scaled_region['x'],
            scaled_region['y'],
            scaled_region['x'] + scaled_region['width'],
            scaled_region['y'] + scaled_region['height']
        ))

        cropped_image_np = np.array(cropped_image)
        result = ocr.ocr(cropped_image_np, cls=True)

        if result:
            text_data.extend(extract_boxes_and_text(result))
        else:
            text_data.append({"text": "No text detected in this region", "box": scaled_region, "confidence": 0})
    return text_data


# --- OCR Endpoint ---
@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        file = request.files['file']
        regions = json.loads(request.form['regions'])
        original_width = int(request.form['original_width'])
        original_height = int(request.form['original_height'])

        # Generate unique filename with timestamp and UUID
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        file.save(file_path)

        text_data = []

        image = Image.open(file_path)
        text_data.extend(process_image(image, regions, original_width, original_height))
        image.close()  # Ensure the file is closed after processing

        print(f"File saved: {file_path}")
        return jsonify({
            "message": "Text extraction successful",
            "data": text_data,
            "file_path": file_path
        })

    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Run Flask Server ---
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
