from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, RadioField, DecimalField
from wtforms.validators import DataRequired

# TODO: bei den SelectFields bei denen keine Zahlen zur weiteren verarbeitung genutzt werden, kein verwenden von zahlen
# -> würde code in routes.py besser verständlich machen

class FileForm(FlaskForm):
    file = FileField(validators=[DataRequired('no File found')])
    colorfile = FileField()
    # TODO: Werte für low, medium, high anpassen
    quality = SelectField('Quality', choices = [(1,'low'),(3,'medium'),(4,'high')], coerce= int,validators=[DataRequired()])
    matrixtype = SelectField('Matrix-Type', choices = [(2,'U-Matrix'),(3,'P-Matrix')], coerce= int,validators=[DataRequired()])
    colortype  = SelectField('Color-Type', choices = [(2,'Not Political'),(3,'Political')], coerce= int,validators=[DataRequired()])
    experience = SelectField('Settings', choices = [(2,'Easy-Mode'),(3,'Expert-Mode')], coerce= int,validators=[DataRequired()])
    submit = SubmitField('Next', id="submitfield")


class ScaleForm(FlaskForm):
    x = DecimalField(validators = [DataRequired()], id='xvalue')
    y = DecimalField(validators = [DataRequired()], id='yvalue')
    z = DecimalField(validators = [DataRequired()], id='zvalue')
    submit = SubmitField('Apply')

class ColorForm(FlaskForm):
    colorscheme = SelectField('Color-Scheme', choices = [(2,'Geographical'),(3,'Heatmap'),(4,'Political')], coerce= int,validators=[DataRequired()], id ='colorschemevalue')
    offset =  DecimalField(validators = [DataRequired()], id='offsetvalue')
    layerwidth =  DecimalField(validators = [DataRequired()], id='layervalue')
    colorfile = FileField()
    submit = SubmitField('Apply')
