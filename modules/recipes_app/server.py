from flask import Flask, render_template, request, redirect, flash, send_file
from werkzeug.utils import secure_filename
import json
import os


UPLOAD_FOLDER = './images/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/image/<name>')
def get_image(name):
    return send_file(os.path.join('images', name), as_attachment=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_url, recipes = process_image(filename)

            return render_template('result.html',
                                   image_url=image_url, recipes=recipes)
    return render_template('index.html')


def process_image(from_image_url):
    to_image_url = from_image_url
    recipes = [{'name': 'Rec1', 'ingredients': [
        'a', 'b', 'c', 'd'], 'preparation': 'Do something'}]

    return to_image_url, recipes

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.run(debug=True)
