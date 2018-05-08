import os
from flask import Flask, request, redirect, url_for ,flash,render_template
from werkzeug.utils import secure_filename
from disease_detection import Disease_Detection


UPLOAD_FOLDER = 'D:/projects/Plant_Disease_Detection/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("-----", filename)

            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('index.html')

@app.route('/show' ,methods = ['POST', 'GET'])
def show():
    #please pass the list of images within the results parameters
    return Disease_Detection( UPLOAD_FOLDER )



if __name__ == "__main__":
   app.run(debug = True)