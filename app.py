from fileinput import filename
from re import S
from flask import Flask, render_template, request, redirect,flash, send_file
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from PIL import Image
import os

UPLOAD_FOLDER="static/uploads/"

app=Flask(__name__)

ROOT = app.instance_path[0:-8]

app.secret_key="secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.route('/arena/compressor',methods=["GET",])
def compressor():
    # delete all images in root folder
    imgs = []
    for file in os.listdir(ROOT):
        if file.endswith(".jpg"):
            imgs.append(file)

    for img in imgs:
        os.remove(img)
    
    return render_template('compressor.html')

@app.route('/arena/compress',methods=["POST",])
def compress():
    uploaded_file=request.files['file']
    size_req=request.form['size']
    if uploaded_file.filename!='':
        uploaded_file.save(UPLOAD_FOLDER+uploaded_file.filename)
        img=Image.open(uploaded_file)
        from compress import compress_image
        compress_image(img,size_req, uploaded_file.filename)

    return render_template('download.html')

@app.route('/download_file',methods=["GET",])
def download():
    # find .jpg in root folder

    for file in os.listdir(ROOT):
        if file.endswith(".jpg"):
            return send_file(file, as_attachment=True)
    return "Error 404"



if __name__ == "__main__":
    app.run(debug=True, port=7000)