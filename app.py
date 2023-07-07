from flask import Flask, render_template, request, redirect, url_for
import os
# import urllib.request
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.secret_key = "encoder@file"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 # 10 MB limit

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/experience")
def experience():
    return render_template("experience.html")

@app.route("/contribute")
def github():
    return render_template("contribute.html")

@app.route("/help")
def help():
    return render_template("help.html")

# A function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# A route to handle the file upload
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('experience'))
    else:
        return "File not allowed"

if __name__ == "__main__":
    app.run(debug=True)
    