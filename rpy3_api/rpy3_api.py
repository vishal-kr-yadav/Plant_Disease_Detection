#!flask/bin/python
import os
from flask import Flask, request, render_template, jsonify

from textblob import TextBlob
from marshmallow import Schema, fields
from flask_restful import Resource, Api
from forms_text import text_api, file_upload
from werkzeug.utils import secure_filename

from codes.sudoku import display, solve
from codes.pdf import pdf_miner

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
UPLOAD_PATH = 'tmp/'

class BlobSchema(Schema):
    polarity = fields.Float()
    subjectivity = fields.Float()
    chunks = fields.List(fields.String, attribute="noun_phrases")
    tags = fields.Raw()
    discrete_sentiment = fields.Method("get_discrete_sentiment")
    word_count = fields.Function(lambda obj: len(obj.words))

    def get_discrete_sentiment(self, obj):
        if obj.polarity > 0.1:
            return 'positive'
        elif obj.polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'

blob_schema = BlobSchema()

class analyzeText(Resource):
    def post(self):
        blob = TextBlob(request.form['data'])
        result = blob_schema.dump(blob)
        return result.data
    
api.add_resource(analyzeText, '/v1/api/text')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text_api', methods=['GET', 'POST'])
def analyze_text():
    form = text_api()
    if form.validate_on_submit():
        text = form.text.data
        blob = TextBlob(text)
        result = blob_schema.dump(blob)
        return render_template('api.html', form=form, data=result.data)

    return render_template('api.html', form=form)

@app.route('/about_me')
def about_me():
    return render_template('cv.html')

@app.route('/sudoku', methods=['GET', 'POST'])
def sudoku():
    form_s = text_api()
    if form_s.validate_on_submit():
        text = form_s.text.data
        if len(text)==81:
            try:
                data = solve(text)
            except:
                text = [text[i:i+9] for i in range(0, 80, 9)]
                message = "Its 99.99% more likely that you have made some mistake while inputting sudoku string. And 0.01% that we could not slove. Please check your sudoku..."
                return render_template('sudoku.html', form=form_s,  message=message, i_data=text)
            
            data = list(data.values())
            data = [data[i:i+9] for i in range(0, 80, 9)]
            text = [text[i:i+9] for i in range(0, 80, 9)]
        else:
            message = "Total no of character in input should be 81, with .(dot) and number. You have submited {} characters.".format(len(text))
            text = [text[i:i+9] for i in range(0, 80, 9)]
            return render_template('sudoku.html', form=form_s,  message=message, i_data=text)
        return render_template('sudoku.html', form=form_s, data=data, i_data=text)

    return render_template('sudoku.html', form=form_s)


##sudako api
class sudokuAPI(Resource):
    def post(self):
        text = request.form['data']
        if len(text)==81:
            try:
                data = solve(text)
            except:
                message = "Please check your sudoku. Its 99.99% more likely that you have made some mistake while inputting sudoku string. And 0.01% that we could not slove. Please check your sudoku. Web interface at http://bkrmdahal.pythonanywhere.com/sudoku"
                return {"Error":message}
            data = list(data.values())
            data = [data[i:i+9] for i in range(0, 80, 9)]
            return {"solution":data}
        else:
            return {"Error":"Total no of character in input should be 81, with .(dot) and number. You have submited {} characters.".format(len(text))}

api.add_resource(sudokuAPI, '/v1/api/sudoku')

#added the pdf mining
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['pdf']

@app.route('/pdf', methods=['GET', 'POST'])
def pdfparsing():
    form_s = file_upload()
    if form_s.fileName.data:
        file = request.files[form_s.fileName.name]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        if allowed_file(filename):
            data, text = pdf_miner(os.path.join(app.config['UPLOAD_PATH'], filename))
        else:
            return render_template('pdf.html', form=form_s, message="Please uploaded pdf file")

        return render_template('pdf.html', form=form_s, data=data, text=text)
    else:
        return render_template('pdf.html', form=form_s)

if __name__=='__main__':
    app.run(debug=True)