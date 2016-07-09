#!/usr/bin/python
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

# app = Flask(__name__,  static_url_path = "uploads", static_folder = "uploads")
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/mit/mdeyo/web_scripts/uploads/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS





@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
    # return render_template('hello.html', name=name, image=send_from_directory("uploads","motivation_fear.jpg"))


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
 		# will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


@app.route('/', methods=['GET','POST'])
def generic():
    return 'Hello, World'

if __name__ == "__main__":
    app.run(debug = True, port = 8080, host='0.0.0.0')
