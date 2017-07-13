from flask import Flask, request, render_template, jsonify, make_response
import imghdr
import xml.etree.cElementTree as et
from cairosvg import svg2png

app = Flask(__name__)


@app.route('/images/upload', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'GET':
        # render template for uploading image
        return render_template('upload.html')
    
    elif request.method == 'POST':
        try:
            _file = request.files['file']
            image, file_name, content_type = handle_image(_file)

            # create response with image
            response = make_response(image)

            response.headers['Content-Type'] = content_type
            # after uncomment line below, response will save image to disk
            # response.headers['Content-Disposition'] = 'attachment; filename=file_name' 

            return response

        except:
            # error msg if nothing was uploaded
            return jsonify({
                'status': 'error',
                'msg': 'No image uploaded or wrong format file'
            })


def handle_image(input_file):
    '''Check uploaded files and choose what to do next'''
    filename = input_file.filename
    raw_img = input_file.stream.read() # bytes string
    try:
        if is_svg(raw_img):
            png_img = svg_to_png(raw_img) # if file is svg convert it to png
            return png_img, '{0}.png'.format(filename.split('.')[0]), 'image/png'

    except:
        file_format = imghdr.what(filename, h=raw_img) # Detect if file is image
        if file_format is None:
            # error if file is not image
            raise Exception('Not image!')
        else:
            return raw_img, filename, 'image/{0}'.format(file_format)


def is_svg(file):
    '''Detect if file is svg'''
    tag = None

    try:
        for x in et.fromstring(file):
            tag = x.tag
            break
    except et.ParseError:
        pass
    return '{http://www.w3.org/2000/svg}' in tag

def svg_to_png(raw_svg):
    '''Convert svg image to png format'''
    png_img = svg2png(bytestring=raw_svg)

    return png_img

if __name__ == '__main__':
    app.run(port=5000, debug=True)