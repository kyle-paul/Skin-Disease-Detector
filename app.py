import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash 
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from datetime import datetime
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
import os
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['SECRET_KEY'] = "hacker@hackathon"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 # 10 MB limits

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_forms.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Load models
model_path = 'archive/best_model_and_weights/fine-tune-model.pb/fine-tune-model.h5'
classes = ['Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis', 'Dermatofibroma', 'Melanoma', 'Melanocytic nevi', 'Vascular ']
model = tf.keras.models.load_model(model_path)
user_name_login = None
email_login = None
login_check = False

@app.route("/")
def home():
    return render_template("home.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/user_guildance/website_guildance")
def website_guildance():
    return render_template("website_guildance.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/user_guildance/download_guildance")
def download_guildance():
    return render_template("download_guildance.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/home/data_gathering")
def data_gathering():
    return render_template("data_gathering.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/home/training_process")
def training_process():
    return render_template("training_process.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/home/result_metrics")
def result_metrics():
    return render_template("result_metrics.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/home/ultimate_goal")
def ultimate_goal():
    return render_template("ultimate_goal.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/experience", methods=["GET"])
def experience():
    return render_template("experience.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route("/edit_img", methods=["GET"])

def edit_img():
    return render_template("edit_img.html", user_name_login=user_name_login, email_login=email_login, login_check=login_check)

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
        return render_template('experience.html', image_path=image_path, progress_bar_animated=True, user_name_login=user_name_login, email_login=email_login, login_check=login_check) 
    else: 
        return "File not allowed"

@app.route("/predict", methods=["GET", "POST"]) 
def predictor(): 
    image_path = session.get('image_path') 
    if image_path: 
        img = cv2.imread(image_path) 
        img = cv2.resize(img, (160, 160)) 
        result = model.predict(img.reshape(1, 160, 160, 3)) 
        class_indx = np.argmax(result[0]) 
        return render_template('experience.html', prediction=classes[class_indx], image_path=image_path, progress_bar_animated=True, user_name_login=user_name_login, email_login=email_login, login_check=login_check) 
    else: return "No image uploaded"
    
# Create a model (database)
class UsersDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(200), nullable=False, unique=True)
    user_name = db.Column(db.String(200), unique=True)
    description =  db.Column(db.String(200))
    password_hash = db.Column(db.String(200))
    @property
    def password():
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name

# Create the registration form
class Registration(FlaskForm):
    name = StringField("Enter your name:", validators=[DataRequired()])
    email = StringField("Enter your email:", validators=[DataRequired()])
    user_name = StringField("Enter your user name:", validators=[DataRequired()])
    password_hash = PasswordField("Enter your password:", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField("Confirm your password:", validators=[DataRequired()])
    submit = SubmitField("Register now")    

# Create the login form
class Login(FlaskForm):
    email = StringField("Enter your email:", validators=[DataRequired()])
    password_hash = PasswordField("Enter your password:", validators=[DataRequired()])
    submit = SubmitField("Login now")    

@app.route("/login", methods=["GET", "POST"]) 
def login():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = Login()
    # Validate form
    if form.validate_on_submit():        
        email = form.email.data
        password = form.password_hash.data
        pw_to_check = UsersDB.query.filter_by(email=email).first()
        passed = check_password_hash(pw_to_check.password_hash, password)
        if passed == True:
            global user_name_login
            global email_login
            global login_check
            user_name_login = pw_to_check.user_name
            email_login = pw_to_check.email
            login_check = True
        
        form.email.data = ''
        form.password_hash.data = ''
    return render_template("login.html", email=email, form=form, password=password, pw_to_check=pw_to_check, passed=passed)

@app.route("/registration", methods=["GET", "POST"]) 
def registration():
    email = None
    form = Registration()
    # Validate form
    if form.validate_on_submit():
        user_name = UsersDB.query.filter_by(user_name=form.user_name.data).first()
        email = UsersDB.query.filter_by(user_name=form.email.data).first()
        if user_name is None and email is None:
            # Hash password
            hased_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = UsersDB(name=form.name.data, email=form.email.data, user_name=form.user_name.data, password_hash=hased_pw)
            db.session.add(user)
            db.session.commit()
        email = form.email.data
        form.name.data = ''
        form.email.data = ''
        form.user_name.data = ''
        form.password_hash.data = ''
    registration_form = UsersDB.query.order_by(UsersDB.date_added)
    return render_template("registration.html", email=email, form=form, registration_form=registration_form)

    
# Create a Response form 
class ResponseForm(FlaskForm):
    name = StringField("Enter your name:", validators=[DataRequired()])
    email = StringField("Enter your email:", validators=[DataRequired()])
    description = StringField("Enter your description:", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
@app.route("/add_form", methods=["GET", "POST"]) 
def add_form():
    name = None
    form = ResponseForm()
    # Validate form
    if form.validate_on_submit():
        userform = UsersDB.query.filter_by(email=form.email.data).first()
        if userform is None:
            userform = UsersDB(name=form.name.data, email=form.email.data, description=form.description.data)
            db.session.add(userform)
            db.session.commit()
        else:
            if request.method == "POST":
                userform.name = request.form['name']
                userform.email = request.form['email']
                userform.description = request.form['description']
                db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.description.data = ''
        flash("Form Submitted Successfully!")
    our_user_forms = UsersDB.query.order_by(UsersDB.date_added)
    return render_template("add_form.html", name=name, form=form, our_user_forms=our_user_forms, delete=False, user_name_login=user_name_login, email_login=email_login, login_check=login_check)

@app.route('/update_form/<int:id>', methods=["GET", "POST"])
def update_form(id):
    form = ResponseForm()
    form_to_update = UsersDB.query.get_or_404(id)
    if request.method == "POST":
        form_to_update.name = request.form['name']
        form_to_update.email = request.form['email']
        form_to_update.description = request.form['description']
        try:
            db.session.commit()
            flash("Form information has been updated successfully!")
            return render_template("update_form.html", form_to_update=form_to_update, form=form)
        except:
            flash("Failure: form information can not be updated!")
            return render_template("update_form.html", form_to_update=form_to_update, form=form)
    else:
        return render_template("update_form.html", form_to_update=form_to_update, form=form, user_name_login=user_name_login, email_login=email_login, login_check=login_check)
        
@app.route('/delete_form/<int:id>', methods=["GET", "POST"])
def delete_form(id):
    name = None
    form = ResponseForm()
    form_to_delete = UsersDB.query.get_or_404(id)
    
    try:
        db.session.delete(form_to_delete)
        db.session.commit()
        flash("Form has been deleted successfully!")
        our_user_forms = UsersDB.query.order_by(UsersDB.date_added)
        return render_template("add_form.html", name=name, form=form, our_user_forms=our_user_forms, delete=True)
    except:
        flash("There is a problem! Please try again")
        return render_template("add_form.html", name=name, form=form, our_user_forms=our_user_forms, user_name_login=user_name_login, email_login=email_login, login_check=login_check)
            

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
    