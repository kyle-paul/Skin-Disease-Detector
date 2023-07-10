import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for, jsonify, session 
import os
from PIL import Image
# import urllib.request
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.secret_key = "encoder@file"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 # 10 MB limit

# Load model
model_path = 'archive/best_model_and_weights/fine-tune-model.pb/fine-tune-model.h5'
classes = ['Actinic keratoses and intraepithelial carcinoma', 'basal cell carcinoma', 'benign keratosis-like lesions', 'dermatofibroma', 'melanoma', 'melanocytic nevi', 'vascular lesions']
model = tf.keras.models.load_model(model_path)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/experience", methods=["GET"])
def experience():
    return render_template("experience.html")

@app.route("/edit_img", methods=["GET"])
def edit_img():
    return render_template("edit_img.html")

# A function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route("/upload", methods=["POST"]) 
def uploader(): 
    imagefile = request.files['imagefile'] 
    if imagefile.filename == '': 
        return render_template('experience.html', progress_bar_animated=False, not_file=True)
    if imagefile and allowed_file(imagefile.filename): 
        filename = secure_filename(imagefile.filename) 
        image_path = "static/uploads/" + imagefile.filename 
        imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        session['image_path'] = image_path 
        return render_template('experience.html', image_path=image_path, progress_bar_animated=True) 
    else: 
        return "File not allowed"

@app.route("/predict", methods=["GET", "POST"]) 
def predictor(): 
    # get the image path from the session variable 
    image_path = session.get('image_path') 
    if image_path: 
        img = cv2.imread(image_path) 
        img = cv2.resize(img, (160, 160)) 
        result = model.predict(img.reshape(1, 160, 160, 3)) 
        class_indx = np.argmax(result[0]) 
        return render_template('experience.html', prediction=classes[class_indx], image_path=image_path, progress_bar_animated=True) 
    else: return "No image uploaded"
    
    

if __name__ == "__main__":
    app.run(debug=True)
    