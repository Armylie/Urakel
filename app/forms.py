from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, RadioField, DecimalField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = FileField(validators=[DataRequired('no File found')])
    quality = SelectField('Quality', choices = [(2,'low'),(3,'medium'),(4,'high')], coerce= int,validators=[DataRequired()])
    submit = SubmitField('Next')

# TODO: Input U-Matrix oder P-Matrix über Form (evtl. RadioButton)
class UPForm(FlaskForm):
    choice = RadioField(choices = ['U-Matrix','P-Matrix'])

class ScaleForm(FlaskForm):
    x = DecimalField(validators = [DataRequired()])
    y = DecimalField(validators = [DataRequired()])
    z = DecimalField(validators = [DataRequired()])
    unit = SelectField('Unit', choices = [(1,'mm'),(2,'px')], coerce = int, validators =[DataRequired()])
    submit = SubmitField('Apply')

