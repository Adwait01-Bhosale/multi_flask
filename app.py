from re import S
from flask import Flask, render_template, request, redirect,flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from PIL import Image
from compress import compress_image
import os

UPLOAD_FOLDER="static/uploads"
app=Flask(__name__)

app.secret_key="secret_key"
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS=set(['png','jpg','jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.split('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/arena')
def new():
    return render_template('main.html')

@app.route('/arena/compressor',methods=["GET","POST"])

def compress():
    # uploaded_file=request.files['file']
    # size_req=request.form['size']
    # if uploaded_file.filename!='':
    #     uploaded_file.save(uploaded_file.filename)
    #     img=Image.open(uploaded_file)
    return render_template('compressor.html')        
if __name__ == "__main__":
    app.run(debug=True, port=7000)