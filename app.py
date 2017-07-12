from flask import Flask, request, render_template, send_from_directory
import os
import shutil
from svg_to_png import svg_to_png

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # Repository path


@app.route('/images/upload')
def index():
    return render_template('upload.html') # Template for uploading images


@app.route('/images/uploaded', methods=['POST'])
def upload_img():
    '''Post method for upload images'''
    target = os.path.join(APP_ROOT, 'images/')  #  Empty folder for upload images
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.mkdir(target)

    path = os.path.join(APP_ROOT, 'static/')    # Empty folder for converted images
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


    try:
        for file in request.files.getlist('file'):
            filename = file.filename
            destination = '/'.join([target, filename])
            file.save(destination)
            svg_to_png(destination, filename)       # Converting function

    except:
        return render_template('error.html')        # Error template for none image uploaded

    else:
        return get_gallery()


@app.route('/images/<filename>')
def send_image(filename):
    '''Response'''
    return send_from_directory('static',filename)


@app.route('/images/uploaded', methods=['POST'])
def get_gallery():
    '''Displays images on websites'''
    images = os.listdir('./static/')
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
