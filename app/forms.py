from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, RadioField, DecimalField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = FileField(validators=[DataRequired('no File found')])
    colorfile = FileField()
    quality = SelectField('Quality', choices = [(1,'low'),(2,'medium'),(3,'high')], coerce= int,validators=[DataRequired()])
    matrixtype = SelectField('Matrix-Type', choices = [('UMatrix','U-Matrix'),('PMatrix','P-Matrix')], id='matrixvalue', coerce= str,validators=[DataRequired()])
    colortype  = SelectField('Color-Type', choices = [('notpolit','Gradient'),('polit','Political')], coerce= str,validators=[DataRequired()])
    experience = SelectField('Settings', choices = [('easy','Easy-Mode'),('expert','Expert-Mode')], coerce= str,validators=[DataRequired()])
    submit = SubmitField('Next', id="submitfield")


class ScaleForm(FlaskForm):
    x = DecimalField(validators = [DataRequired()],number_format=float, id='xvalue')
    y = DecimalField(validators = [DataRequired()], id='yvalue')
    z = DecimalField(validators = [DataRequired()], id='zvalue')
    submit = SubmitField('Apply', id="applycolor")

class ColorForm(FlaskForm):
    colorscheme = SelectField('Color-Scheme', choices = [('UMatrix','Geographical'),('PMatrix','Heatmap'),('polit','Political')], coerce= str,validators=[DataRequired()])
    offset =  DecimalField(id='offsetvalue')
    layerwidth =  DecimalField(validators = [DataRequired()], id='layervalue')
    colorfile = FileField()
    submit = SubmitField('Apply', id="applyscale")

class ExportForm(FlaskForm):
    submit = SubmitField('Export', id="exportsubmit")
