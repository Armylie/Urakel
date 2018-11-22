from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import FileForm, ScaleForm
from app import Main
import os

# allgemeiner Pfad zum Zwischenspeichern von Dateien (natürlich bei jedem User individuell)
PATH = "C:\\Users\\Sara\\Desktop\\Upload"
COLOURS = ['altitude scale', 'heatmap', 'white']
SCALES = ['mm', 'px']
ACTPATH = "\"C:\\Users\\Sara\\Desktop\\Upload\\UStar_trans.stl\"" # nur temporär, später  = ''


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FileForm()
    if form.validate_on_submit():
        name = form.file.data.filename
        inpath = os.path.join(PATH, name)
        form.file.data.save(inpath) # Zwischenspeichern der Datei # TODO: Datenbank?
        outpath = inpath.replace('.stl', '_trans.stl')
        Main.trans([inpath, outpath, str(form.quality.data)])
        ACTPATH = outpath # so kann später mit diesem Ergebnis weiter gearbeitet werden
        return render_template('umatrixmodify.html', title='U-Matrix', colours=COLOURS)
    return render_template('index.html', title='Home', form=form)


@app.route('/umatrixmodify', methods=['GET', 'POST'])
def umatrixmodify():
    return render_template('umatrixmodify.html', title='U-Matrix', colours=COLOURS)


@app.route('/pmatrixmodify', methods=['GET', 'POST'])
def pmatrixmodify():
    return render_template('pmatrixmodify.html', title='P-Matrix', colours=COLOURS)


@app.route('/scaleandsave', methods=['GET', 'POST'])
def scaleandsave():
    form = ScaleForm()
    dims = Main.scale([ACTPATH,ACTPATH,'3'])
    print(dims)
    form.x.data = dims[0]
    form.y.data= dims[1]
    form.z.data = dims[2]
    if form.validate_on_submit():
        # TODO: führe Skalierung aus
        return render_template('scaleandsave.html', title='Scale and Save', form=form)
    return render_template('scaleandsave.html', title='Scale and Save', form = form)

# @app.route('/popup')
# def user_popup():
#    return render_template('popup.html', title='Popup-Hilfe')
