import os
import shutil
import zipfile
from flask import flash, redirect, render_template, url_for, send_from_directory, make_response
from app import Main, app
from app.forms import FileForm, ScaleForm, ColorForm, ExportForm
from functools import update_wrapper

def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

# delete all files in Temp
def clearTemp():
    for i in os.listdir(__file__.replace('routes.py', 'Temp')):
        os.remove(os.path.join(__file__.replace('routes.py', 'Temp'), i))

# if not already existing, generate directory for temporary storage
# otherwise ensure that it is empty
if not os.path.isdir(__file__.replace('routes.py', 'Temp')):
    os.mkdir(__file__.replace('routes.py', 'Temp'))
else:
    clearTemp()

# delete zipfile from a previous use of the program
if os.path.isfile(__file__.replace('routes.py', 'Temp.zip')):
    os.remove(__file__.replace('routes.py', 'Temp.zip'))

# names of the textures
UTEX = "UmatrixTexture"
PTEX  = "PmatrixTexture"

# paths to store the .stl file and if necessary the mapping of the political coloring
MATPATH =__file__.replace('routes.py', os.path.join('Temp','Matrix.stl'))
COLORPATH = __file__.replace('routes.py', os.path.join('Temp','Island.txt'))

# path for showing the 3d file at coloring and export mode
RENDERPATH = __file__.replace('routes.py', os.path.join('static','Matrix.stl'))

# parameters for matrix processing, choosen by the user
matrixtype, colortype, experience, quali = "","","",""
# default values for offset and layerwidth of the coloring, change by user is possible
offset = 0
layerwidth = 1.7



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    clearTemp()
    global MATPATH, COLORPATH, matrixtype, colortype, experience, quali
    form = FileForm()
    if form.validate_on_submit():
        # check whether the given file is of the correct type (.stl)
        if (form.file.data.filename.endswith('.stl')):
            form.file.data.save(MATPATH) # save the file temporary

            # save the parameters for later use
            matrixtype = form.matrixtype.data
            colortype = form.colortype.data
            experience = form.experience.data
            quali = str(form.quality.data)

            # saving additional file if colortype is political
            if colortype == 'polit':
                # check whether the given file is of the correct type (.txt)
                if form.colorfile.data.filename.endswith('.txt'):
                    form.colorfile.data.save(COLORPATH)
                else:
                    print("Missing or invalid mapping for political coloring. Please add correct mapping or choose 'not political'.")
                    flash("Missing or invalid mapping for political coloring. Please add correct mapping or choose 'not political'.")
                    return render_template('index.html', title='Home', form=form)

            Main.trans([MATPATH, MATPATH, quali, RENDERPATH]) # basic transformation of the matrix

            # switch by mode (easy: additional coloring of the matrix, expert: direct forwarding to the next page)
            if experience == 'easy':
                outpath = MATPATH.replace('.stl', '.obj')
                # switch by colortype (political/not political)
                if colortype == 'polit':
                    Main.color_political([MATPATH, outpath, COLORPATH, quali])
                else:
                    # UMatrix
                    if matrixtype == 'UMatrix':
                        Main.color_geographic([MATPATH, outpath, UTEX, str(layerwidth), str(offset), quali])
                    # PMatrix
                    else:
                        Main.color_geographic([MATPATH, outpath, PTEX, str(layerwidth), str(offset), quali])
                return redirect('/saveandexport')

            # expert mode
            return redirect('/scale')

        else:
            print('Invalid file format. Please choose a .stl file.')
            flash('Invalid file format. Please choose a .stl file.')
            return render_template('index.html', title='Home', form=form)

    return render_template('index.html', title='Home', form=form)


@app.route('/colormodify', methods=['GET', 'POST'])
def colormodify():
    global colortype, layerwidth, offset, matrixtype, quali, COLORPATH
    form = ColorForm()

    # save new parameters
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

    outpath = MATPATH.replace('.stl', '.obj')
    # switch by colortype (political/UMatrix/PMatrix)
    if colortype == 'polit':
        # check whether there is already an existing mapping for the political coloring
        if os.path.isfile(COLORPATH):
            # if there is another mapping -> update COLORFILE
            if form.colorfile.data.filename.endswith('.txt'):
                os.remove(COLORPATH)
                form.colorfile.data.save(COLORPATH)
            # coloring
            Main.color_political([MATPATH, outpath, COLORPATH, quali])
        # no existing file but a new one
        elif form.colorfile.data.filename.endswith('.txt'):
            form.colorfile.data.save(COLORPATH)
            # coloring
            Main.color_political([MATPATH, outpath, COLORPATH, quali])
        else: # no mapping found
            print("Missing or invalid mapping for political coloring. Please add correct mapping or choose 'geographical' or 'heatmap'.")
            flash("Missing or invalid mapping for political coloring. Please add correct mapping or choose 'geographical' or 'heatmap'.")
            return render_template('colormodify.html', title='Color', form=form)
    # normal coloring, using parameters given by the user or default values
    else:
        if matrixtype == 'UMatrix':
            Main.color_geographic([MATPATH, outpath, UTEX, str(layerwidth), str(offset), quali])
        else:
            Main.color_geographic([MATPATH, outpath, PTEX, str(layerwidth), str(offset), quali])

    # display the parameters
    form.offset.data = offset
    form.layerwidth.data = layerwidth
    if colortype == 'polit':
        form.colorscheme.data = 'polit'
    else:
        form.colorscheme.data = matrixtype

    return render_template('colormodify.html', title='Color', form = form)



@app.route('/popup')
def user_popup():
    return render_template('popup.html', title='Popup-Hilfe')

@app.route('/render', methods=['GET', 'POST'])
#@nocache
def render_3d():
    resp = make_response(render_template('Rendering/index.html', title='Render'))
    resp.cache_control.no_cache = True
    return resp

@app.route('/scale', methods=['GET', 'POST'])
def scale():
    form = ScaleForm()

    # scale the matrix
    if form.validate_on_submit():
        # save additional Matrix for 3d View
        # z.data = base + z = 1/4 * z + z = 5/4 * z   <=> z = 4/5 * z.Data
        Main.scale([RENDERPATH, RENDERPATH, '0', str(form.x.data), str(form.y.data), str(form.z.data*4/5)])

        Main.scale([MATPATH, MATPATH, '0', str(form.x.data), str(form.y.data), str(form.z.data)])
        return render_template('scale.html', title='Scale and Save', form=form)

    # display the old size of the matrix
    dims = Main.scale([MATPATH, MATPATH, '1'])
    form.x.data = dims[0]
    form.y.data = dims[1]
    form.z.data = dims[2]

    return render_template('scale.html', title='Scale and Save', form = form)


# TODO: Feedback an User?
@app.route('/saveandexport', methods=['GET', 'POST'])
def saveandexport():
    form = ExportForm()

    if form.validate_on_submit():
        # create zip file with final files
        zipper = zipfile.ZipFile(__file__.replace('routes.py', 'Temp.zip'), 'a')
        for i in os.listdir(__file__.replace('routes.py', 'Temp')):
            if i.startswith('Matrix'): # don't save dim and Island
                zipper.write(os.path.join(__file__.replace('routes.py', 'Temp'), i), i, zipfile.ZIP_DEFLATED)
        zipper.close()

        clearTemp() # clear cache

        return send_from_directory(__file__.replace('routes.py', ''),'Temp.zip')

    return render_template('saveandexport.html', title='Save and Export',form = form)

