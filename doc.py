from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS  # Import CORS
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import os
import json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_boxes_and_text(results):
    """Extract only box coordinates and text from OCR results."""
    extracted_data = []
    if results is None:
        return extracted_data  # Return empty list if results is None
    
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
    regions = json.loads(request.form['regions'])
    original_width = int(request.form['original_width'])  # Send the original image width from frontend
    original_height = int(request.form['original_height'])  # Send the original image height from frontend

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
                print("Original Region:", region)

                # Scale the region coordinates to match the full-size image
                scaling_factor_x = image.width / original_width
                scaling_factor_y = image.height / original_height

                # Adjust coordinates based on the scaling factor
                scaled_region = {
                    'x': region['x'] * scaling_factor_x,
                    'y': region['y'] * scaling_factor_y,
                    'width': region['width'] * scaling_factor_x,
                    'height': region['height'] * scaling_factor_y,
                }

                # Crop the image based on the adjusted region
                cropped_image = image.crop((
                    scaled_region['x'], 
                    scaled_region['y'], 
                    scaled_region['x'] + scaled_region['width'], 
                    scaled_region['y'] + scaled_region['height']
                ))

                # # Save the cropped image temporarily to inspect it
                # cropped_image.save('cropped_image.png')

                # Convert PIL Image to numpy array for PaddleOCR
                cropped_image_np = np.array(cropped_image)

                # Run OCR on the cropped image
                result = ocr.ocr(cropped_image_np, cls=True)
                # Only process result if it's not None or empty
                if result and len(result) > 0:  
                    text_data.extend(extract_boxes_and_text(result))
                else:
                    # Handle the case where no text is detected in the region
                    text_data.append({"text": "No text detected in the selected region", "box": scaled_region, "confidence": 0})

    else:
        # Process image directly
        image = Image.open(file_path)
        for region in regions:
            print("Original Region:", region)

          # Initialize scaled_region before using it
            scaled_region = region.copy()  # Create a copy to ensure original region is not modified

            # Scale the region coordinates to match the full-size image
            scaling_factor_x = image.width / original_width
            scaling_factor_y = image.height / original_height

            # If the frontend has already scaled the coordinates, undo the scaling
            if scaling_factor_x != 1 or scaling_factor_y != 1:
                scaled_region['x'] = region['x'] / scaling_factor_x
                scaled_region['y'] = region['y'] / scaling_factor_y
                scaled_region['width'] = region['width'] / scaling_factor_x
                scaled_region['height'] = region['height'] / scaling_factor_y

            # Crop the image based on the adjusted region
            cropped_image = image.crop((
                scaled_region['x'], 
                scaled_region['y'], 
                scaled_region['x'] + scaled_region['width'], 
                scaled_region['y'] + scaled_region['height']
            ))

            print("Cropped Region:", scaled_region)

            # Save the cropped image temporarily to inspect it
            cropped_image.save('cropped_image.png')

            # Convert PIL Image to numpy array for PaddleOCR
            cropped_image_np = np.array(cropped_image)

            # Run OCR on the cropped image
            result = ocr.ocr(cropped_image_np, cls=True)
            
            # Handle None or empty result or result with None inside it
            if result and isinstance(result, list):
                # Filter out None values
                result = [line for line in result if line is not None]
                
                if len(result) > 0:
                    text_data.extend(extract_boxes_and_text(result))
                else:
                    text_data.append({"text": "No text detected", "box": {}, "confidence": 0})
            else:
                text_data.append({"text": "No text detected", "box": {}, "confidence": 0})


    return jsonify({"data": text_data})


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
