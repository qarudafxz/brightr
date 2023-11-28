# Import necessary libraries
from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

app = Flask(__name__)

height = 128
width = 128
channels = 3

# api endpoint to test the server
@app.route('/api/adjust_hsl', methods=['POST'])
def adjust_hsl_endpoint():
    data = request.json

    # extract file paths from the request data
    file_paths = data.get('file_paths', [])

    # convert file paths to numpy arrays
    uploaded_images_np = [cv2.imread(file_path) for file_path in file_paths]

    # converting images to HSL format
    hsl_images = [cv2.cvtColor(img, cv2.COLOR_BGR2HLS) for img in uploaded_images_np]

    #adjusting the original hsl values of image to the hsl values returned from regression model
    adjusted_images = adjust_hsl_values(hsl_images, model)
    
    adjusted_images_base64 = [cv2.imencode('.jpg', img)[1].tobytes().decode('utf-8') for img in adjusted_images]

    # Return adjusted images to the frontend
    return jsonify(adjusted_images_base64)

# read images from file paths
def read_images(file_paths):
    images = [cv2.imread(file_path) for file_path in file_paths]
    return images

# adjust HSL values of an image
def adjust_hsl_values(hsl_imgs, model):
    adjusted_hsl_imgs = []
    
    for img in hsl_imgs:
        h, l, s = cv2.split(img)
    
        img_array = np.array([h, l, s]).reshape(1, height, width, 3)
    
        predicted_hsl = model.predict(img_array)
    
        predicted_h, predicted_s, predicted_l = predicted_hsl[0]
        
        h = h + predicted_h
        s = s + predicted_s
        l = l + predicted_l
  
        h = np.clip(h, 0, 255)
        s = np.clip(s, 0, 255)
        l = np.clip(l, 0, 255)
        
        adjusted_img = cv2.merge((h, l, s))
        adjusted_hsl_imgs.append(adjusted_img)
    
    return adjusted_hsl_imgs

# Regression model
model = keras.Sequential([
    layers.Conv2D(64, (3, 3), activation='relu', input_shape=(height, width, channels)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(3)  # Output layer for HSL values
])

model.compile(optimizer='adam', loss='mean_squared_error')

if __name__ == '__main__':
    app.run(debug=True)
