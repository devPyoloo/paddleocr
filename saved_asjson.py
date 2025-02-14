import numpy as np
import cv2
import matplotlib.pyplot as plt
import json

# Paths for input and saved images
input_img_path = 'uploads/HC202001-E_eng_1.png'
saved_img_path = 'uploads/VC201501-E-clp-chi_1.png'

# Load the images
input_img = cv2.imread(input_img_path)
saved_img = cv2.imread(saved_img_path)

# Convert images to grayscale
input_img_bw = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
saved_img_bw = cv2.cvtColor(saved_img, cv2.COLOR_BGR2GRAY)

# Display the input image
rgb_saved_image = cv2.cvtColor(saved_img_bw, cv2.COLOR_BGR2RGB)
plt.imshow(rgb_saved_image)
plt.title("Input Image")
plt.show()

# Initialize the ORB detector algorithm
orb = cv2.ORB_create()

# Detect keypoints and compute descriptors
savedKeypoints, savedDescriptors = orb.detectAndCompute(saved_img_bw, None)

# Function to convert KeyPoint objects to serializable dictionaries
def keypoints_to_serializable(keypoints):
    return [
        {
            "pt": kp.pt,  # Keypoint coordinates (x, y)
            "size": kp.size,  # Diameter of the meaningful keypoint region
            "angle": kp.angle,  # Orientation of the keypoint (-1 if not applicable)
            "response": kp.response,  # Keypoint response (used for ranking)
            "octave": kp.octave,  # Octave (pyramid layer) in which the keypoint was detected
            "class_id": kp.class_id,  # Object class (if available)
        }
        for kp in keypoints
    ]

# Convert keypoints to a serializable format
savedKeypoints_serializable = keypoints_to_serializable(savedKeypoints)

# Convert descriptors to a list
if savedDescriptors is not None:
    savedDescriptors_serializable = savedDescriptors.tolist()
else:
    savedDescriptors_serializable = []

# Combine keypoints and descriptors into a single dictionary
saved_features = {
    "keypoints": savedKeypoints_serializable,
    "descriptors": savedDescriptors_serializable,
}

# Save the features as a JSON file
features_file_path = 'saved_features.json'
with open(features_file_path, 'w') as json_file:
    json.dump(saved_features, json_file)

print(f"Features saved to {features_file_path}")
print(f"Saved Descriptors Shape: {np.shape(savedDescriptors)}")
