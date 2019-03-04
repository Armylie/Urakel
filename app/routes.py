import os

from flask import flash, redirect, render_template, url_for

from app import Main, app
from app.forms import FileForm, ScaleForm, ColorForm, ExportForm

os.mkdir(__file__.replace('routes.py', 'Temp')) # erstelle Ordner zum Zwischenspeichern

# Namen der Texturen
UTEX = "UmatrixTexture"
PTEX  = "PmatrixTexture"

# Pfade für .stl Datei der Matrix und ggf. Mapping zur politischen Färbung
MATPATH =__file__.replace('routes.py', 'Temp\\Matrix.stl')
COLORPATH = __file__.replace('routes.py', 'Temp\\Matrix.txt')

# vom Nutzer gewählte Parameter zur weiteren Verarbeitung der Matrix
matrixtype, colortype, experience, quali = "","","",""
# Defaultwerte für offset und layerwidth, spätere Änderung vom Nutzer möglich
offset = 0.15 # TODO: andere Defaultwerte auch in Color.py
layerwidth = 1.63  # TODO: andere Defaultwerte auch in Color.py



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global MATPATH, COLORPATH, matrixtype, colortype, experience, quali
    form = FileForm()
    if form.validate_on_submit():
        form.file.data.save(MATPATH) # Zwischenspeichern der .stl Datei der Matrix

        quali = str(form.quality.data)

        matrixtype = form.matrixtype.data
        colortype = form.colortype.data
        experience = form.experience.data
        # COLORFILE speichern
        #TODO: Abfrage funktioniert so nicht??
        # if colortype == 3:
        if form.colorfile.data.filename != "":
            form.colorfile.data.save(COLORPATH)

        Main.trans([MATPATH, MATPATH, quali]) # Grundtransformation (glätten etc.) der Matrix

        # easy mode:
        if experience == 'easy':
            outpath = MATPATH.replace('.stl', '.obj')
            # politische Färbung
            if colortype == 'polit':
                Main.color_political([MATPATH, outpath, COLORPATH, quali])
            # normale Färbung ohne Parameter
            else:
                # UMatrix
                if matrixtype == 'UMatrix':
                    Main.color_geographic([MATPATH, outpath, UTEX, str(layerwidth), str(offset)])
                # PMatrix
                else:
                    Main.color_geographic([MATPATH, outpath, PTEX, str(layerwidth), str(offset)])
            return redirect('/saveandexport')

        # expert mode
        return redirect('/scale')
    return render_template('index.html', title='Home', form=form)


@app.route('/colormodify', methods=['GET', 'POST'])
def colormodify():
    global colortype, layerwidth, offset, matrixtype, quali

    form = ColorForm()
    # neue Wert abspeichern
    if form.validate_on_submit():
        layerwidth = form.layerwidth.data
        offset = form.offset.data
        if form.colorscheme.data == 'polit': # wenn political
            colortype = 'polit'
        elif form.colorscheme.data == 'heat': # heat-map
            colortype = 'notpolit'
            matrixtype = 'PMatrix'
        else: # geographical
            colortype = 'notpolit'
            matrixtype = 'UMatrix'

    #Färbung
    outpath = MATPATH.replace('.stl', '.obj')
    # politische Färbung
    if colortype == 'polit':
        Main.color_political([MATPATH, outpath, COLORPATH, quali])
    # normale Färbung ohne Parameter
    else:
        # UMatrix
        if matrixtype == 'UMatrix':
            Main.color_geographic([MATPATH, outpath, UTEX, str(layerwidth), str(offset)])
        # PMatrix
        else:
            Main.color_geographic([MATPATH, outpath, PTEX, str(layerwidth), str(offset)])

    # Anzeige der bisherigen Werte
    form.offset.data = offset
    form.layerwidth.data = layerwidth
    if colortype == 'polit': #political
        form.colorscheme.data = 'polit'
    else: form.colorscheme.data = matrixtype
    return render_template('colormodify.html', title='Color', form = form)


@app.route('/saveandexport', methods=['GET', 'POST'])
def saveandexport():
    form = ExportForm()
    if form.validate_on_submit():
        # TODO: save final files at given path

        # lösche alle Dateien in Temp und Temp selbst
        for i in os.listdir(__file__.replace('routes.py', 'Temp')):
            os.remove(os.path.join(__file__.replace('routes.py', 'Temp'), i))
        os.rmdir(__file__.replace('routes.py', 'Temp'))

    return render_template('saveandexport.html', title='Save and Export',form = form)

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
        Main.scale([MATPATH, MATPATH, '0', str(form.x.data), str(form.y.data), str(form.z.data)])
        return render_template('scale.html', title='Scale and Save', form=form)
    dims = Main.scale([MATPATH, MATPATH, '1'])
    form.x.data = dims[0]
    form.y.data = dims[1]
    form.z.data = dims[2]
    return render_template('scale.html', title='Scale and Save', form = form)
