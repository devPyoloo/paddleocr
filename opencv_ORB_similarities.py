import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle

# Paths for images and saved features
input_img_path = 'uploads/invoice2.png'
saved_img_path = 'uploads/water-supply.jpg'
saved_features_path = 'saved_features.pkl'

# Load input and saved images
input_img = cv2.imread(input_img_path)
saved_img_bw = cv2.imread(saved_img_path, cv2.IMREAD_GRAYSCALE)

if input_img is None or saved_img_bw is None:
    print("Error: One of the images could not be loaded.")
    exit()

# Convert input image to grayscale
input_img_bw = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

### 🔹 Step 1: Preprocessing to Improve Keypoint Detection ###
# Apply Gaussian Blur (removes noise)
input_img_bw = cv2.GaussianBlur(input_img_bw, (3, 3), 0)

# Apply Adaptive Histogram Equalization (CLAHE) for better contrast
clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
input_img_bw = clahe.apply(input_img_bw)

# Show the preprocessed image
plt.imshow(cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB))
plt.title("Preprocessed Input Image")
plt.show()

# Load saved keypoints and descriptors
try:
    with open(saved_features_path, 'rb') as saved_file:
        savedKeypoints_serialized, savedDescriptors = pickle.load(saved_file)
except FileNotFoundError:
    print("Error: Saved features file not found.")
    exit()

# Function to convert serialized keypoints back to cv2.KeyPoint objects
def serializable_to_keypoints(serialized_keypoints):
    return [cv2.KeyPoint(
                x=kp["pt"][0], 
                y=kp["pt"][1], 
                size=kp["size"], 
                angle=kp.get("angle", -1), 
                response=kp.get("response", 0), 
                octave=kp.get("octave", 0), 
                class_id=kp.get("class_id", -1)) 
            for kp in serialized_keypoints]

# Convert serialized keypoints
savedKeypoints = serializable_to_keypoints(savedKeypoints_serialized)

# Initialize ORB
orb = cv2.ORB_create()

# Detect keypoints and descriptors in input image
inputKeypoints, inputDescriptors = orb.detectAndCompute(input_img_bw, None)

# Ensure descriptors exist
if inputDescriptors is None or savedDescriptors is None:
    print("Error: Unable to compute descriptors.")
    exit()

# Match descriptors using BFMatcher with KNN
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
matches = matcher.knnMatch(inputDescriptors, savedDescriptors, k=2)

# Apply Lowe's ratio test
good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

# Sort matches by quality
good_matches = sorted(good_matches, key=lambda x: x.distance)

# Draw top 20 matches
final_img = cv2.drawMatches(input_img_bw, inputKeypoints,
                            saved_img_bw, savedKeypoints,
                            good_matches[:20], None)

# Resize while maintaining aspect ratio
h, w = final_img.shape[:2]
scale = 1000 / w
final_img = cv2.resize(final_img, (int(w * scale), int(h * scale)))

# Display matches
cv2.imshow("Matches", final_img)
cv2.waitKey(9000)
cv2.destroyAllWindows()

# Determine similarity percentage
match_percentage = len(good_matches) / len(savedDescriptors) * 100
print(f"Match Percentage: {match_percentage:.2f}%")

# Dynamic similarity threshold
# Lower value (e.g., 5%) → More invoices will be considered similar
# Higher value (e.g., 20-30%) → Stricter matching, fewer invoices will be considered similar
threshold_percentage = 15  # Adjust based on tests
if match_percentage > threshold_percentage:
    print("The input invoice is similar to the saved invoice!")
else:
    print("The input invoice is not similar to the saved invoice.")
