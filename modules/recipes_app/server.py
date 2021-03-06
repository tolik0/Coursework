from flask import Flask, render_template, request, redirect, flash, \
    send_from_directory
from werkzeug.utils import secure_filename
import torch
import json
import os
import sys
from datetime import datetime

sys.path.append('../')
from dishes_finder import find_dishes
from prefinal import detector

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/image/<name>')
def get_image(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               name)


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

            image_url, recipes, ingredients = process_image(
                os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print(os.getcwd())
            return render_template('result.html',
                                   image_url=image_url, recipes=recipes,
                                   fruits=ingredients)
    return render_template('index.html')


def process_image(from_image_url):
    to_image_url = "res{}.jpg".format(str(datetime.now()).
                                      replace(":", "-").replace(" ", ""))
    print('from url: ', from_image_url)
    ingredients = detector(model, from_image_url, to_image_url)

    recipes = []
    dishes = find_dishes(ingredients)
    for dish in dishes:
        recipes.append({'name': dish._name, 'ingredients':
            dish.get_ingredients(), 'preparation': 'do something'})
    return to_image_url, recipes, ingredients


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = 'super secret key'
    model_path = "../mymodel_finetuning_new_v1.pth"
    model = torch.load(model_path)
    print(os.getcwd())

    app.run(debug=True)
