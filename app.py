# Import libraries and helper functions
import os
import requests
import subprocess
from flask import Flask, render_template, request
from helpers import extract_ingredient_names, search_complex_recipe, identifier
from ultralytics import YOLO
from werkzeug.utils import secure_filename

# configure aplication
app = Flask(__name__)
# Temporary directory to store uploaded images
app.config['UPLOAD_FOLDER'] = 'uploads/'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/', methods=['GET', 'POST'])
def complex_search():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # predict the image file
            output = identifier(filepath)
            # Extract the detected ingredients from the output
            ingredients = extract_ingredient_names(output)
            # get recipies 
            if ingredients:
                recipes = search_complex_recipe(ingredients=ingredients)
            # print(recipes)
            # Process your output here
            return render_template('results.html', recipes=recipes, ingredients=ingredients)
    return render_template('index.html')
