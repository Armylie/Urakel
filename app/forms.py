from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, RadioField, DecimalField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = FileField(validators=[DataRequired('no File found')])
    colorfile = FileField()
    # TODO: Werte für low, medium, high anpassen
    quality = SelectField('Quality', choices = [(1,'low'),(3,'medium'),(4,'high')], coerce= int,validators=[DataRequired()])
    matrixtype = SelectField('Matrix-Type', choices = [('UMatrix','U-Matrix'),('PMatrix','P-Matrix')], coerce= str,validators=[DataRequired()])
    colortype  = SelectField('Color-Type', choices = [('notpolit','Not Political'),('polit','Political')], coerce= str,validators=[DataRequired()])
    experience = SelectField('Settings', choices = [('easy','Easy-Mode'),('expert','Expert-Mode')], coerce= str,validators=[DataRequired()])
    submit = SubmitField('Next', id="submitfield")


class ScaleForm(FlaskForm):
    x = DecimalField(validators = [DataRequired()], id='xvalue')
    y = DecimalField(validators = [DataRequired()], id='yvalue')
    z = DecimalField(validators = [DataRequired()], id='zvalue')
    submit = SubmitField('Apply')

class ColorForm(FlaskForm):
    colorscheme = SelectField('Color-Scheme', choices = [('geo','Geographical'),('heat','Heatmap'),('polit','Political')], coerce= str,validators=[DataRequired()], id ='colorschemevalue')
    offset =  DecimalField(validators = [DataRequired()], id='offsetvalue')
    layerwidth =  DecimalField(validators = [DataRequired()], id='layervalue')
    colorfile = FileField()
    submit = SubmitField('Apply')
