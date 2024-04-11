# Import libraries and helper functions
import json
import os
import requests
import subprocess
import whisper
from flask import Flask, render_template, request, jsonify
from helpers import extract_ingredient_names, search_complex_recipe, identifier, process_command
from ultralytics import YOLO
from werkzeug.utils import secure_filename

# configure aplication
app = Flask(__name__)
# Temporary directory to store uploaded images
app.config['UPLOAD_FOLDER'] = 'uploads/'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

model = whisper.load_model("base.en") 

@app.route('/', methods=['GET', 'POST'])
def complex_search():
    if request.method == 'POST':
        # Initialize a dictionary to hold parameters for search_complex_recipe
        # print("We got here")
        params = {}
        ingredients = None
        # Extract query text input (if provided)
        query = request.form.get('query')
        if query:
            params['query'] = query
        
        # Process file upload (if provided)
        file = request.files.get('file')
        # print(file, file.filename)
        # file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file through identifier to get ingredients
            output = identifier(filepath)
            # print("identified")
            if output is None:
                return jsonify({"error": "Could not run the file: " + filename})
            # print(output)
            
            # Extract the detected ingredients from the output
            ingredients = extract_ingredient_names(output)
            if ingredients:
                params['force_ingredients'] = ingredients

        # Add additional form parameters to params as needed
        # For example, if you have a dietary restriction input:
        # diet = request.form.get('diet')
        # if diet:
        #     params['diet'] = diet.split(',')  # Assuming multiple diets can be separated by commas
        
        # Now call search_complex_recipe with dynamic params
        recipes = search_complex_recipe(**params)
        
        if recipes:
            # recipes = json.dumps(recipes)
            return jsonify({"ingredients_found": ingredients, "recipes": recipes}) if ingredients else jsonify({"recipes": recipes})

        else:
            return jsonify({"error": "No recipes found"})
        print(recipes)
        # Process your output here
        return render_template('results.html', recipes=recipes, ingredients=ingredients)
    return render_template('index.html')

@app.route('/audio', methods=['POST'])
def handle_audio():
    audio_file = request.files['audio']
    audio_file.save("temp.wav")  # Save the received audio file
    result = model.transcribe("temp.wav")  # Transcribe the audio
    text = result['text']
    # print(text)
    params, ingredients = process_command(text)
    if params:
        recipes= search_complex_recipe(**params)
        # print("params: ")
        # print(params)
        # print(recipes)
        if recipes:
            # recipes = json.dumps(recipes)
            return jsonify({"ingredients_found": ingredients, "recipes": recipes}) if ingredients else jsonify({"recipes": recipes})
        else:
            return jsonify({"error": "No recipes found"})