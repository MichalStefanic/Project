from flask import Flask, request, render_template, send_from_directory
import os
import shutil
from svg_to_png2 import svg_to_png

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/images/upload", methods=['GET', 'POST'])
def upload_img():
    if request.method == 'GET':
        return render_template("upload2.html")
    
    elif request.method == 'POST':

        target = os.path.join(APP_ROOT, "images/")
        if os.path.isdir(target):
            shutil.rmtree(target)
        os.mkdir(target)

        path = os.path.join(APP_ROOT, "static/")
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)

        try:
            _file = request.files["file"]
            filename = _file.filename
            destination = "/".join([target, filename])
            _file.save(destination)
            my_path, my_format, img_name = svg_to_png(destination, filename)
            return send_from_directory('static', img_name, mimetype='image/.{0}'.format(my_format))

        except:
            return render_template("error.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    