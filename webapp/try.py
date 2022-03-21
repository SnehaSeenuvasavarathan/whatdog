import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import io
import numpy as np
import cv2
model = load_model('model_0.h5')
newsize = (200,200)
breeds = ['silky_terrier', 'Scottish_deerhound', 'Chesapeake_Bay_retriever', 'Ibizan_hound',
 'wire', 'Saluki', 'cocker_spaniel', 'schipperke', 'borzoi', 'Pembroke', 'komondor', 'Staffordshire_bullterrier', 
 'standard_poodle', 'Eskimo_dog', 'English_foxhound', 'golden_retriever', 'Sealyham_terrier', 'Japanese_spaniel', 
 'miniature_schnauzer', 'malamute']

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    im=Image.open(file)
    im=im.resize((200,200))
    print(im)
    img=np.array(im)
    print(img, img.shape)
    img = np.reshape(img, (1,200,200,3))
    output = model.predict(img)[0]
    prediction= breeds[np.argmax(output, axis=0)]
    
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash(prediction)
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
    
if __name__ == "__main__":
    app.run()