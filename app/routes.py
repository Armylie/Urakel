import os

from flask import flash, redirect, render_template, url_for

from app import Main, app
from app.forms import FileForm, ScaleForm, ColorForm

# öffnen der 'Datenbank'
# TODO: SAVEPATH und TEXTUREPATH aus Datenbank rausschmeißen? (nur Blenderpath nötig?)
with open(__file__.replace('routes.py','paths.txt')) as file:
    data = eval(file.read())


# allgemeiner Pfad zum Zwischenspeichern von Dateien
PATH = data.get('SAVEPATH')
UTEX = "UmatrixTexture"
PTEX = "PmatrixTexture"
# verwendete Variablen, werden an entsprechender Stelle überschrieben
ACTPATH ="" # TODO: nutze zum Zwischenspeichern festen Namen (unabhängig von Namen der Eingabedatei)
COLORFILE = ""
matrixtype = 0
colortype = 0
colorparams = False
offset = 0.15 # TODO: andere Defaultwerte auch in Color.py
layerwidth = 1.63  # TODO: andere Defaultwerte auch in Color.py
experience = 0
quali = ""


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global ACTPATH, matrixtype, colortype, experience, COLORFILE, quali
    form = FileForm()
    if form.validate_on_submit():
        name = form.file.data.filename
        inpath = os.path.join(PATH, name)
        form.file.data.save(inpath) # Zwischenspeichern der Datei
        outpath = inpath.replace('.stl', '_trans.stl')
        quali = str(form.quality.data)
        Main.trans([inpath, outpath, quali])
        ACTPATH = outpath # so kann später mit diesem Ergebnis weiter gearbeitet werden
        matrixtype = form.matrixtype.data
        colortype = form.colortype.data
        experience = form.experience.data
        # COLORFILE speichern
        #TODO: Abfrage funktioniert so nicht??
        # if colortype == 3:
        if form.colorfile.data.filename != "":
            COLORFILE = os.path.join(PATH, form.colorfile.data.filename)

        # easy mode:
        if experience == 2:
            outpath = ACTPATH.replace('.stl', '.obj')
            # politische Färbung
            if colortype == 3:
                Main.color_political([ACTPATH,outpath,COLORFILE,quali])
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


@app.route('/colormodify', methods=['GET', 'POST'])
def colormodify():
    global colortype, colorparams, layerwidth, offset, matrixtype, quali

    form = ColorForm()
    # neue Wert abspeichern
    if form.validate_on_submit():
        layerwidth = form.layerwidth.data
        offset = form.offset.data
        if form.colorscheme.data == 4: # wenn political
            colortype = 3
        elif form.colorscheme.data == 3: # heat-map
            colortype = 2
            matrixtype = 3
        else: # geographical
            colortype = 2
            matrixtype = 2
        colorparams = True

    #Färbung
    outpath = ACTPATH.replace('.stl', '.obj')
    # politische Färbung
    if colortype == 3:
        Main.color_political([ACTPATH, outpath, COLORFILE,quali])
    # normale Färbung ohne Parameter
    else:
        # UMatrix
        if matrixtype == 2:
            if colorparams:
                Main.color_geographic([ACTPATH,outpath,UTEX,'1',str(layerwidth),str(offset)])
            else:
                Main.color_geographic([ACTPATH, outpath, UTEX, '0'])
        # PMatrix
        else:
            if colorparams:
                Main.color_geographic([ACTPATH,outpath,PTEX,'1',str(layerwidth),str(offset)])
            else:
                Main.color_geographic([ACTPATH, outpath, PTEX, '0'])

    # Anzeige der bisherigen Werte
    form.offset.data = offset
    form.layerwidth.data = layerwidth
    if colortype == 3: #political
        form.colorscheme.data = 4
    else: form.colorscheme.data = matrixtype
    return render_template('colormodify.html', title='Color', form = form)


@app.route('/saveandexport', methods=['GET', 'POST'])
def saveandexport():
    # TODO: save final files at given path
    # TODO: delete all other files
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
        Main.scale([ACTPATH,ACTPATH,'0',str(form.x.data),str(form.y.data),str(form.z.data)])
        return render_template('scale.html', title='Scale and Save', form=form)
    dims = Main.scale([ACTPATH, ACTPATH, '1'])
    form.x.data = dims[0]
    form.y.data = dims[1]
    form.z.data = dims[2]
    return render_template('scale.html', title='Scale and Save', form = form)
