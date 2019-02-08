from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, RadioField, DecimalField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = FileField(validators=[DataRequired('no File found')])
    colorfile = FileField()
    # TODO: Werte für low, medium, high anpassen
    quality = SelectField('Quality', choices = [(1,'low'),(3,'medium'),(4,'high')], coerce= int,validators=[DataRequired()])
    matrixtype = SelectField('Matrix-Type', choices = [(2,'U-Matrix'),(3,'P-Matrix')], coerce= int,validators=[DataRequired()])
    colortype  = SelectField('Color-Type', choices = [(2,'Not Political'),(3,'Political')], coerce= int,validators=[DataRequired()])
    experience = SelectField('Settings?', choices = [(2,'Easy-Mode'),(3,'Expert-Mode')], coerce= int,validators=[DataRequired()])
    submit = SubmitField('Next')

# TODO: Input U-Matrix oder P-Matrix über Form (evtl. RadioButton)
class UPForm(FlaskForm):
    choice = RadioField(choices = ['U-Matrix','P-Matrix'])

class ScaleForm(FlaskForm):
    x = DecimalField(validators = [DataRequired()], id='xvalue')
    y = DecimalField(validators = [DataRequired()], id='yvalue')
    z = DecimalField(validators = [DataRequired()], id='zvalue')
    unit = SelectField('Unit', choices = [(1,'mm'),(2,'px')], coerce = int, validators =[DataRequired()])
    submit = SubmitField('Apply')

class ColorForm(FlaskForm):
    colorscheme = SelectField('Color-Scheme', choices = [(2,'Geographical'),(3,'Heatmap'),(4,'White')], coerce= int,validators=[DataRequired()])
    offset = SelectField('Offset', choices = [(2,'Geographical'),(3,'Heatmap'),(4,'White')], coerce= int,validators=[DataRequired()])
    layerwidth = SelectField('Layer-Width', choices = [(2,'Geographical'),(3,'Heatmap'),(4,'White')], coerce= int,validators=[DataRequired()])
    submit = SubmitField('Apply')
