# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import os
import base64

app = Flask(__name__)
CORS(app)

@app.route('/api/adjust_brightness', methods=['POST'])
def adjust_brightness_endpoint():
    try:
  
        uploaded_images = request.files.getlist('images')


        file_paths = [save_uploaded_file(image) for image in uploaded_images]

    
        adjusted_images = [adjust_brightness(preprocess_image(file_path)) for file_path in file_paths]

        adjusted_images_base64 = [image_to_base64(img) for img in adjusted_images]

   
        for i, adjusted_img in enumerate(adjusted_images):
            cv2.imwrite(file_paths[i], adjusted_img)
        

        return jsonify(adjusted_images_base64, {'success': 'Images adjusted successfully!'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong!'})

def save_uploaded_file(file):
    file_path = os.path.join("../uploads", file.filename)
    file.save(file_path)
    return file_path

def preprocess_image(file_path):
    # Read and resize the image to the expected size
    img = cv2.imread(file_path)
    return img

def adjust_brightness(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    l, a, b = cv2.split(lab)
    
    # Adjust the lightness channel
    l = cv2.add(l, 40)
    
    # Adjust the contrast (curve) of the lightness channel
    l = cv2.convertScaleAbs(l, alpha=1.2, beta=10) 
    
    adjusted_img = cv2.merge((l, a, b))
    
    return cv2.cvtColor(adjusted_img, cv2.COLOR_LAB2BGR)

def image_to_base64(img):
    # Convert image to base64 for easy transfer to the frontend
    return base64.b64encode(cv2.imencode('.jpg', img)[1]).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
