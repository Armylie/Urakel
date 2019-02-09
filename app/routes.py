import os

from flask import flash, redirect, render_template, url_for

from app import Main, app
from app.forms import FileForm, ScaleForm, ColorForm

# öffnen der 'Datenbank'
# TODO: öffnen über relativen Pfad
with open('C:\\Users\\Sara\\Desktop\\Neuer Ordner\\Urakel\\app\\paths.txt') as file:
    data = eval(file.read())


# allgemeiner Pfad zum Zwischenspeichern von Dateien
PATH = data.get('SAVEPATH')
COLOURS = ['altitude scale', 'heatmap', 'white']
ACTPATH =""
matrixtype = 0
colortype = 0
experience = 0
COLORFILE = ""
UTEX = "UmatrixTexture"
PTEX = "PmatrixTexture"


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global ACTPATH, matrixtype, colortype, experience, COLORFILE
    form = FileForm()
    if form.validate_on_submit():
        name = form.file.data.filename
        inpath = os.path.join(PATH, name)
        form.file.data.save(inpath) # Zwischenspeichern der Datei
        outpath = inpath.replace('.stl', '_trans.stl')
        Main.trans([inpath, outpath, str(form.quality.data)])
        ACTPATH = outpath # so kann später mit diesem Ergebnis weiter gearbeitet werden
        matrixtype = form.matrixtype.data
        colortype = form.colortype.data
        experience = form.experience.data

        # COLORFILE speichern
        if form.colorfile.data.filename != "":
            COLORFILE = os.path.join(PATH, form.colorfile.data.filename)

        # easy mode:
        if experience == 2:
            outpath = ACTPATH.replace('.stl', '.obj')
            # politische Färbung
            if colortype == 3:
                Main.color_political([ACTPATH,outpath,COLORFILE])
            # normale Färbung ohne Parameter
            else:
                # UMatrix
                if matrixtype == 2:
                    Main.color_geographic([ACTPATH,outpath,UTEX,'0'])
                # PMatrix
                else:
                    Main.color_geographic([ACTPATH, outpath, PTEX, '0'])
            return redirect('/saveandexport')

        # expert mode
        return redirect('/scale')
    return render_template('index.html', title='Home', form=form)


@app.route('/umatrixmodify', methods=['GET', 'POST'])
def umatrixmodify():
    return render_template('umatrixmodify.html', title='U-Matrix', colours=COLOURS)


@app.route('/pmatrixmodify', methods=['GET', 'POST'])
def pmatrixmodify():
    return render_template('pmatrixmodify.html', title='P-Matrix', colours=COLOURS)


@app.route('/saveandexport', methods=['GET', 'POST'])
def saveandexport():
    return render_template('saveandexport.html', title='Save and Export')

@app.route('/popup')
def user_popup():
    return render_template('popup.html', title='Popup-Hilfe')

@app.route('/render', methods=['GET', 'POST'])
def render_3d():
    return render_template('Rendering/index.html', title='Render')

@app.route('/scale', methods=['GET', 'POST'])
def scale():
    form = ScaleForm()
    if form.validate_on_submit():
        print(ACTPATH)
        Main.scale([ACTPATH,ACTPATH,'0',str(form.x.data),str(form.y.data),str(form.z.data)])
        return render_template('scale.html', title='Scale and Save', form=form)
    dims = Main.scale([ACTPATH, ACTPATH, '1'])
    form.x.data = dims[0]
    form.y.data = dims[1]
    form.z.data = dims[2]
    # TODO: über next richtige Weiterleitung entsprechend bei Start gewählter Parameter
    return render_template('scale.html', title='Scale and Save', form = form)
