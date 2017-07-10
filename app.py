from flask import Flask, request, render_template, send_from_directory
import os
from svg_to_png import svg_to_png

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, "images/")
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)

	for file in request.files.getlist("file"):
		filename = file.filename
		destination = "/".join([target, filename])
		file.save(destination)
		svg_to_png(destination, filename)

	return render_template("complete.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
	return send_from_directory('static',filename)

if __name__ == "__main__":
	app.run(port=5000, debug=True)