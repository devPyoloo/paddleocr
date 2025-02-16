from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import os
import json

app = Flask(__name__)
CORS(app)

ocr = PaddleOCR(use_angle_cls=True, lang='ch', det_db_box_thresh=0.5, det_db_unclip_ratio=2.0)


def preprocess_image(image):
    """Preprocess image to enhance text readability."""
    image_np = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Apply adaptive thresholding
    processed_image = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    return Image.fromarray(processed_image)

def sharpen_image(image):
    image_np = np.array(image)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])  # Sharpening kernel

    sharpened = cv2.filter2D(image_np, -1, kernel)

    return Image.fromarray(sharpened)

def invert_colors(image):
    image_np = np.array(image)
    inverted_image = cv2.bitwise_not(image_np)
    return Image.fromarray(inverted_image)



def extract_header(image):
    """Extract text from the top 20% of the image (header section)."""
    image_width, image_height = image.size
    header_height = int(image_height * 0.20)

    # Crop the header section
    header_image = image.crop((0, 0, image_width, header_height))

    # Preprocess images
    processed_images = [
        header_image,
        preprocess_image(header_image),
        sharpen_image(header_image),
        invert_colors(header_image),
    ]

    extracted_text = []
    for img in processed_images:
        img_np = np.array(img)
        result = ocr.ocr(img_np, cls=True)

        # Extract only the text
        extracted_text.extend([line[1][0] for line in result[0] if len(line) > 1 and line[1]])

    return list(set(extracted_text))  # Remove duplicates



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
