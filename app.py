from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS  # Import CORS
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_boxes_and_text(results):
    """Extract only box coordinates and text from OCR results."""
    extracted_data = []
    for result in results:
        for line in result:
            if len(line) >= 2 and isinstance(line[1], (tuple, list)):
                box = line[0]  # Coordinates
                text_info = line[1]
                
                if len(text_info) >= 1 and isinstance(text_info[0], str):
                    text = text_info[0]  # Extract text
                    extracted_data.append({"box": box, "text": text})
                    # print(f"Box: {box}, Text: {text}")
                else:
                    print(f"Skipping invalid text_info: {text_info}")
            else:
                print(f"Skipping invalid line: {line}")
    return extracted_data


@app.route('/extract-text', methods=['POST'])
def extract_text():
    file = request.files['file']
    regions = request.form['regions']  # Regions as a JSON string
    regions = eval(regions)  # Convert string to list of dicts

    # Save file temporarily
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)  # Ensure the uploads folder exists
    file.save(file_path)

    # Initialize a list to collect text results
    text_data = []

    # If the file is a PDF, convert it to images
    if file.filename.endswith('.pdf'):
        images = convert_from_path(file_path)
        for image in images:
            for region in regions:
                # Crop the image based on the region
                cropped_image = image.crop((
                    region['x'], 
                    region['y'], 
                    region['x'] + region['width'], 
                    region['y'] + region['height']
                ))

                # Convert PIL Image to numpy array for PaddleOCR
                cropped_image_np = np.array(cropped_image)

                # Run OCR on the cropped image
                result = ocr.ocr(cropped_image_np, cls=True)
                text_data.extend(extract_boxes_and_text(result))

    else:
        # Process image directly
        image = Image.open(file_path)
        for region in regions:
            # Crop the image based on the region
            cropped_image = image.crop((
                region['x'], 
                region['y'], 
                region['x'] + region['width'], 
                region['y'] + region['height']
            ))

            cropped_image.save('cropped_image.png')

            # Convert PIL Image to numpy array for PaddleOCR
            cropped_image_np = np.array(cropped_image)

            # Run OCR on the cropped image
            result = ocr.ocr(cropped_image_np, cls=True)
            text_data.extend(extract_boxes_and_text(result))

            print(f"Extracted data: {text_data}")

    return jsonify({"data": text_data})

if __name__ == "__main__":
    app.run(debug=True)
