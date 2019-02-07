import os

from flask import flash, redirect, render_template, url_for

from app import Main, app
from app.forms import FileForm, ScaleForm, ColorForm

# allgemeiner Pfad zum Zwischenspeichern von Dateien (natürlich bei jedem User individuell)
PATH = "C:\\Users\\marc.benjamin.jung\\Documents\\SVN-OrdnerNewwc\\STL" 
COLOURS = ['altitude scale', 'heatmap', 'white']
ACTPATH = "\"C:\\Users\\marc.benjamin.jung\\Documents\\SVN-OrdnerNewwc\\STL\\UStar2_trans.stl\"" # nur temporär, später  = ''


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
        matrixtype = form.matrixtype.data
        colortype = form.colortype.data
        experience = form.experience.data

        # Werte für Skalierungsmaske
        #forms = ScaleForm()
        #dims = Main.scale([ACTPATH, ACTPATH, '3'])
        #forms.x.data = dims[0]
        #forms.y.data = dims[1]
        #forms.z.data = dims[2]
        return redirect('/scale')
        #return render_template('scale.html', title='Skalieren', form = forms) # TODO: Hä? Warum ändert sich die URL nicht?
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
    #dims = Main.scale([ACTPATH, ACTPATH, '3'])
    form.x.data = 5 #dims[0]
    form.y.data = 6 #dims[1]
    form.z.data = 7 #dims[2]
    if form.validate_on_submit():
        # TODO: andere Arten der Skalierung
        print('validate ------------------------------------------------------------')
        Main.scale([ACTPATH,ACTPATH,'0',str(form.x.data),str(form.y.data),str(form.z.data)])
        return render_template('scale.html', title='Scale and Save', form=form)
    #dims = Main.scale([ACTPATH, ACTPATH, '3'])
    #form.x.data = dims[0]
    #form.y.data = dims[1]
    #form.z.data = dims[2]
    return render_template('scale.html', title='Scale and Save', form = form)
