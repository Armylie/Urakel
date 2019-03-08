import os
import zipfile
from flask import flash, redirect, render_template, url_for, send_from_directory
from app import Main, app
from app.forms import FileForm, ScaleForm, ColorForm, ExportForm

# TODO: Hilfetexte in ganzem Programm

# TODO: rufe clearTemp() auf, wenn zurück auf Startseite gewechselt wird (Benny?)
def clearTemp():
    # lösche alle Dateien in Temp
    for i in os.listdir(__file__.replace('routes.py', 'Temp')):
        os.remove(os.path.join(__file__.replace('routes.py', 'Temp'), i))

# erstelle Ordner zum Zwischenspeichern, falls dieser noch nicht existiert, sonst stelle sicher, dass dieser leer ist
if not os.path.isdir(__file__.replace('routes.py', 'Temp')):
    os.mkdir(__file__.replace('routes.py', 'Temp'))
else:
    clearTemp()

# Zip File aus möglichem vorherigen Programmaufruf löschen
# TODO: am Ende des Programms löschen, oder wir verkaufen das als Feature (nach Skye)
if os.path.isfile(__file__.replace('routes.py', 'Temp.zip')):
    os.remove(__file__.replace('routes.py', 'Temp.zip'))

# Namen der Texturen
UTEX = "UmatrixTexture"
PTEX  = "PmatrixTexture"

# Pfade für .stl Datei der Matrix und ggf. Mapping zur politischen Färbung
MATPATH =__file__.replace('routes.py', 'Temp\\Matrix.stl')
COLORPATH = __file__.replace('routes.py', 'Temp\\Island.txt')

# vom Nutzer gewählte Parameter zur weiteren Verarbeitung der Matrix
matrixtype, colortype, experience, quali = "","","",""
# Defaultwerte für offset und layerwidth, spätere Änderung vom Nutzer möglich
offset = 0.15 # TODO: andere Defaultwerte? (nach Skype)
layerwidth = 1.63  # TODO: andere Defaultwerte? (nach Skype)



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # TODO: Bilder einblenden je nach gewählter Aktion?
    # TODO: unable dropdowns nach klicken auf next (Benny?)
    global MATPATH, COLORPATH, matrixtype, colortype, experience, quali
    form = FileForm()
    if form.validate_on_submit():
        # falls die übergebene Datei das passende Format (.stl) hat
        if (form.file.data.filename.endswith('.stl')):
            form.file.data.save(MATPATH) # Zwischenspeichern der .stl Datei der Matrix

            # Parameter zur Matrixverarbeitung speichern
            matrixtype = form.matrixtype.data
            colortype = form.colortype.data
            experience = form.experience.data
            quali = str(form.quality.data)

            # falls politische Färbung gewählt wurde
            if colortype == 'polit':
                # prüfe auf passendes Dateiformat
                if form.colorfile.data.filename.endswith('.txt'):
                    form.colorfile.data.save(COLORPATH)
                else:
                    print("Missing or invalid mapping for political coloring. Please add correct mapping or choose 'not political'.")
                    # TODO: popup (vor Wartebildschirm) (Benny)
                    return render_template('index.html', title='Home', form=form)

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

        else:
            print('Invalid file format. Please choose a .stl file.')
            # TODO: popup (vor Wartebildschirm) (Benny)
            return render_template('index.html', title='Home', form=form)

    return render_template('index.html', title='Home', form=form)


@app.route('/colormodify', methods=['GET', 'POST'])
def colormodify():
    global colortype, layerwidth, offset, matrixtype, quali, COLORPATH
    form = ColorForm()

    # neue Parameter abspeichern
    if form.validate_on_submit():
        layerwidth = form.layerwidth.data
        offset = form.offset.data
        if form.colorscheme.data == 'polit':
            colortype = 'polit'
        elif form.colorscheme.data == 'heat':
            colortype = 'notpolit'
            matrixtype = 'PMatrix'
        else: # geographical
            colortype = 'notpolit'
            matrixtype = 'UMatrix'

    #Färbung der Matrix
    outpath = MATPATH.replace('.stl', '.obj')
    # politische Färbung
    if colortype == 'polit':
        # es wurde bereits eine Datei zur politischen Färbung hochgeladen
        if os.path.isfile(COLORPATH):
            # eine weitere Datei des richtigen Formats wurde hochgeladen -> update COLORFILE
            if form.colorfile.data.filename.endswith('.txt'):
                os.remove(COLORPATH)
                form.colorfile.data.save(COLORPATH)
            # führe Färbung durch
            Main.color_political([MATPATH, outpath, COLORPATH, quali])
        # keine alte Datei vorhanden, aber neue Datei
        elif form.colorfile.data.filename.endswith('.txt'):
            form.colorfile.data.save(COLORPATH)
            # führe Färbung durch
            Main.color_political([MATPATH, outpath, COLORPATH, quali])
        else:
            print("Missing or invalid mapping for political coloring. Please add correct mapping or choose 'geographical' or 'heatmap'.")
            # TODO: popup (vor Wartebildschirm) (Benny)
            return render_template('colormodify.html', title='Color', form=form)
    # normale Färbung, falls Parameter angegeben wurden mit diesen, sonst mit default Werten
    else:
        if matrixtype == 'UMatrix':
            Main.color_geographic([MATPATH, outpath, UTEX, str(layerwidth), str(offset)])
        else:
            Main.color_geographic([MATPATH, outpath, PTEX, str(layerwidth), str(offset)])

    # Anzeige der bisherigen Parameter
    form.offset.data = offset
    form.layerwidth.data = layerwidth
    if colortype == 'polit':
        form.colorscheme.data = 'polit'
    else:
        form.colorscheme.data = matrixtype

    return render_template('colormodify.html', title='Color', form = form)


# TODO: zeige 3D Bild (Sara + Benny, nach Skype)
@app.route('/saveandexport', methods=['GET', 'POST'])
def saveandexport():
    form = ExportForm()

    if form.validate_on_submit():
        # erstelle Zip Ordner mit allen finalen Dateien
        zipper = zipfile.ZipFile(__file__.replace('routes.py', 'Temp.zip'), 'a')
        for i in os.listdir(__file__.replace('routes.py', 'Temp')):
            if i.startswith('Matrix'): # Speichere dim und Island nicht
                zipper.write(os.path.join(__file__.replace('routes.py', 'Temp'), i), i, zipfile.ZIP_DEFLATED)
        zipper.close()

        clearTemp()

        return send_from_directory(__file__.replace('routes.py', ''),'Temp.zip')

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

    # Skalieren der Matrix
    if form.validate_on_submit():
        Main.scale([MATPATH, MATPATH, '0', str(form.x.data), str(form.y.data), str(form.z.data)])
        return render_template('scale.html', title='Scale and Save', form=form)

    # Anzeige der bisherigen Größe
    dims = Main.scale([MATPATH, MATPATH, '1'])
    form.x.data = dims[0]
    form.y.data = dims[1]
    form.z.data = dims[2]

    return render_template('scale.html', title='Scale and Save', form = form)

