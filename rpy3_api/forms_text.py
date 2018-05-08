#!flask/bin/python
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FileField
from wtforms.validators import DataRequired

class text_api(FlaskForm):
    text = StringField('text', validators=[DataRequired()])

class file_upload(FlaskForm):
    fileName = FileField('file', validators=[DataRequired()])