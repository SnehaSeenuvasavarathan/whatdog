import os.path
import numpy as np
import cv2
from PIL import Image, ImageOps
# import requests
from flask import Flask, Response, request
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model('model_0.h5')
newsize = (200,200)

app = Flask(__name__)
app.config.from_object(__name__)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/classify/', methods=['POST'])
def yagaa():
    print("yagaa")
    # file = request.files['dog'].read()
    # file=request.files.get('dog', '')
    file = request.files['dog']
    # file.save('eg.jpg')
    image = file.read()
    # image = Image.open(file)
    # image = np.asarray(image)
    # print(image.shape)
    # print(file)
    # return Response(file)
    # npimg = np.fromstring(file, np.uint8)
    # print(npimg.shape)
    # img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    # im = npimg.resize(newsize)
    # input=np.array(im)
    # output = model.predict(input)
    # print(output)
    return Response(str('pp'))

@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


if __name__ == '__main__':  # pragma: no cover
    app.run(port=8080)
