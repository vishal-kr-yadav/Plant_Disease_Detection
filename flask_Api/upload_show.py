import os
from os import listdir

from flask import Flask, render_template, request
from disease_detection import Disease_Detection
app = Flask(__name__)

UPLOAD_FOLDER = "/home/vishal/Dropbox/ML/Plant_Disease_Detection/queries"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)

    return render_template('index.html')

@app.route('/upload/show', methods=['POST','GET'])
def show():
    return Disease_Detection(UPLOAD_FOLDER)

@app.route('/remove/query/images', methods=['POST','GET'])
def remove():
    filenames = listdir(UPLOAD_FOLDER)
    a = [filename for filename in filenames if filename.endswith('.png')]

    for each in a:
        b = UPLOAD_FOLDER+"/" + each
        os.remove(b)

    return "Removed All Images From Queries Folder"



if __name__ == "__main__":
   app.run(debug = True)