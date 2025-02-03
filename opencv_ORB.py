import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle

# Paths for input and saved images
input_img_path = 'uploads/input.jpg'
saved_img_path = 'uploads/water-supply.jpg'

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
# inputKeypoints, inputDescriptors = orb.detectAndCompute(input_img_bw, None)
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
# inputKeypoints_serializable = keypoints_to_serializable(inputKeypoints)
savedKeypoints_serializable = keypoints_to_serializable(savedKeypoints)


# Save the serialized keypoints and descriptors to files
# with open('input_features.pkl', 'wb') as input_file:
#     pickle.dump((inputKeypoints_serializable, inputDescriptors), input_file)
with open('saved_features.pkl', 'wb') as saved_file:
    pickle.dump((savedKeypoints_serializable, savedDescriptors), saved_file)

# print(f"Input Descriptors Shape: {np.shape(inputDescriptors)}")
print(f"Saved Descriptors Shape: {np.shape(savedDescriptors)}")

# Match the keypoints using BFMatcher
matcher = cv2.BFMatcher()
# matches = matcher.match(inputDescriptors, savedDescriptors)

# Sort matches by distance (best matches first)
# matches = sorted(matches, key=lambda x: x.distance)

# Draw the top 20 matches
# final_img = cv2.drawMatches(input_img_bw, inputKeypoints,
#                             saved_img_bw, savedKeypoints,
#                             matches[:20], None)

# # Resize for better visualization
# final_img = cv2.resize(final_img, (1000, 650))

# # Show the matched image
# cv2.imshow("Matches", final_img)
# cv2.waitKey(5000)  # Wait for 5 seconds
# cv2.destroyAllWindows()

# # Determine similarity based on matches
# similarity_threshold = 30  # Adjust threshold based on experiments
# if len(matches) > similarity_threshold:
#     print("The input invoice is similar to the saved invoice!")
# else:
#     print("The input invoice is not similar to the saved invoice.")
