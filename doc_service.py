from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from flask_cors import CORS
# from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  

ocr = PaddleOCR(use_angle_cls=True, lang='en')

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)



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


def convert_bounding_box_to_full_image(ocr_box, region_x, region_y):
    """Convert OCR bounding box from cropped region back to full image coordinates."""
    full_boxes = []
    for box in ocr_box:
        full_box = [[point[0] + region_x, point[1] + region_y] for point in box]  # adjust coordinates
        full_boxes.append(full_box)
    return full_boxes


def find_matching_region(ocr_box, original_regions):
    """Find the closest matching predefined region for an OCR bounding box."""
    def iou(boxA, boxB):
        """Calculate Intersection over Union (IoU) between two bounding boxes."""
        xA = max(boxA[0][0], boxB['x'])
        yA = max(boxA[0][1], boxB['y'])
        xB = min(boxA[2][0], boxB['x'] + boxB['width'])
        yB = min(boxA[2][1], boxB['y'] + boxB['height'])

        inter_area = max(0, xB - xA) * max(0, yB - yA)
        boxA_area = (boxA[2][0] - boxA[0][0]) * (boxA[2][1] - boxA[0][1])
        boxB_area = boxB['width'] * boxB['height']

        iou_value = inter_area / float(boxA_area + boxB_area - inter_area) if (boxA_area + boxB_area - inter_area) > 0 else 0
        return iou_value

    best_match = None
    max_iou = 0

    for region in original_regions:
        current_iou = iou(ocr_box, region)
        if current_iou > max_iou:
            max_iou = current_iou
            best_match = region

    return best_match


def process_image(image, regions, original_width, original_height):
    """Process image regions and extract text with bounding boxes aligned to full image."""
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
        print(f"OCR Result: {result}")

        if result:
            ocr_text_data = extract_boxes_and_text(result)

            # Convert bounding boxes to full image coordinates and associate with regions
            for data in ocr_text_data:
                full_box = convert_bounding_box_to_full_image([data['box']], scaled_region['x'], scaled_region['y'])
                data['box'] = full_box[0]  # Update bounding box
                
                # Find associated region
                matched_region = find_matching_region(full_box[0], regions)
                if matched_region:
                    data['associated_region'] = matched_region  # Add the original region

            text_data.extend(ocr_text_data)
        else:
            text_data.append({
                "text": "No text detected in this region",
                "box": scaled_region,
                "confidence": 0,
                "associated_region": region
            })
    return text_data


# --- OCR Endpoint ---
@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        # print(f"Incoming files: {request.files}")
        print(f"Incoming form data: {request.form}")
        
        file = request.files['file']
        regions = json.loads(request.form['regions'])
        original_width = int(request.form['original_width'])
        original_height = int(request.form['original_height'])

        text_data = []
        # Open the image directly from memory
        image = Image.open(file.stream)

        # Process the image with OCR
        text_data = process_image(image, regions, original_width, original_height)
        image.close()  # Ensure the file is closed after processing

        print(f"Text Data: {text_data}")
        return jsonify({
            "message": "Text extraction successful",
            "data": text_data
        })

    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Run Flask Server ---
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
