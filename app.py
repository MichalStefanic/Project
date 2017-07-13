from flask import Flask, request, render_template, jsonify, make_response
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
                'msg': 'No image uploaded'
            })


def handle_image(input_file):
    '''Check uploaded files and choose what to do next'''
    filename = input_file.filename
    file_format = input_file.mimetype # get mimetype of file

    if file_format == 'image/svg+xml':
        png_img = svg_to_png(input_file) # if file is svg convert it to png

        return png_img, '{0}.png'.format(filename.split('.')[0]), 'image/png'

    elif 'image' in file_format:
        # if image is in other format just return without changes
        return input_file.stream.read(), filename, file_format

    else:
        # error if file is not image
        raise Exception('Not image!')


def svg_to_png(svg_img):
    '''Convert svg image to png format'''
    raw_svg = svg_img.stream.read()

    png_img = svg2png(bytestring=raw_svg)

    return png_img

if __name__ == '__main__':
    app.run(port=5000, debug=True)