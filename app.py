# Import libraries and helper functions
import os
import requests
import subprocess
from flask import Flask, render_template, request
from helpers import get_full_recipe, extract_ingredient_names
from identify import identifier
from ultralytics import YOLO
from werkzeug.utils import secure_filename

# Select model
best_model = "best.pt"

app = Flask(__name__)
# Temporary directory to store uploaded images
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def whats_in_my_fridge():
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
            recipes = get_full_recipe(ingredients)  
            # print(recipes)
            # Process your output here
            return render_template('results.html', recipes=recipes, ingredients=ingredients)
    return render_template('index.html')


