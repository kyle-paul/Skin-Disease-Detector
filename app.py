from flask import Flask, render_template, request
import urllib.request
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.secret_key = "encoder@file"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10

@app.route("/experience", method=['GET', 'POS'])
def experience():
    return render_template("experience.html")

@app.route("/contribute")
def github():
    return render_template("contribute.html")

@app.route("/help")
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True)
    