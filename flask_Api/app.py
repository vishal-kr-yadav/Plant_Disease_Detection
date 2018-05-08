import os
from os import listdir
import cv2


from flask import Flask, render_template, request
from disease_detection import Disease_Detection
app = Flask(__name__)

UPLOAD_FOLDER = "../queries"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def first():
    return render_template('index.html')




@app.route('/show', methods=['POST'])
def upload_file():
    file = request.files['image']

    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)

    image_name=Disease_Detection(UPLOAD_FOLDER)
    filenames = listdir(UPLOAD_FOLDER)
    a = [filename for filename in filenames if filename.endswith('.png')]

    for each in a:
        b = UPLOAD_FOLDER + "/" + each
        os.remove(b)
    return image_name



if __name__ == "__main__":
   app.run(debug = True)