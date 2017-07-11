from flask import Flask, request, render_template, send_from_directory
import os
from svg_to_png import svg_to_png

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/images/upload")
def index():
	return render_template("upload.html")

@app.route("/images/uploaded", methods=['POST'])
def upload_img():
	target = os.path.join(APP_ROOT, "images/")
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)
	try:
		for file in request.files.getlist("file"):
			filename = file.filename
			destination = "/".join([target, filename])
			file.save(destination)
			svg_to_png(destination, filename)
	except:
		return render_template("Error.html")
	else:
		return get_gallery()

@app.route('/images/<filename>')
def send_image(filename):
	return send_from_directory('static',filename)

@app.route('/images/gallery', methods=['POST'])
def get_gallery():
	images = os.listdir("./static/")
	return render_template("gallery.html", images=images)

if __name__ == "__main__":
	app.run(port=5000, debug=True)