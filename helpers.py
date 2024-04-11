# Import libraries
import inflect
import os
import pandas as pd
import re
import requests
import subprocess
import spacy

from keys import Global_Variables
from ultralytics import YOLO

# Setup model and image
globalVar = Global_Variables()
# image_path = "static/foods1.jpg"
best_model = globalVar.obj_model
# Global variables api_key
api_key = globalVar.RECIPE_API

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")
p = inflect.engine()

# Define lists for cuisines, intolerances, meal types, and diets
cuisines_list = ["African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", 
                 "Eastern European", "European", "French", "German", "Greek", "Indian", 
                 "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", 
                 "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", 
                 "Spanish", "Thai", "Vietnamese"]

intolerances_list = ["Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood", "Sesame",
                     "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"]

meal_types_list = ["main course", "side dish", "dessert", "appetizer", "salad", "bread",
                   "breakfast", "soup", "beverage", "sauce", "marinade", "fingerfood",
                   "snack", "drink"]

diets_list = ["Gluten Free", "Ketogenic", "Vegetarian", "Lacto-vegetarian", "Ovo-vegetarian",
              "Vegan", "Pescetarian", "Paleo", "Primal", "Low FODMAP", "Whole30"]

exclusion_keywords = ["allergic", "remove", "exclude", "no", "without"]

# Load the CSV file, specifying no headers and the correct delimiter
file_path = 'static/top-1k-ingredients.csv'
ingredients_data = pd.read_csv(file_path, header=None, delimiter=';')

# Extract only the first column, which contains the ingredient names
ingredients_list = ingredients_data[0].tolist()
singular_ingredients = {p.singular_noun(ing) or ing for ing in ingredients_list}


# function to run a cli prediction on a given image
def identifier(img):
      # CLI for inference
      cmd = f"yolo task=detect mode=predict model={best_model} conf=0.25 source={img} save=False"

      # Run the inference command and capture the output
      result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
      
      return result.stderr if result.stderr is not None else None


# Extract identified ingredients from a terminal output
def extract_ingredient_names(yolov8_output):
    # Extracting the part of the string after the resolution (e.g., "704x800")
    ingredients_part = re.search(r"\d+x\d+ (.+)", yolov8_output).group(1)
    
    # Pattern to match only ingredient names
    pattern = r"\d+ ([a-zA-Z\s]+)"
    
    # Find all matches in the extracted part
    matches = re.findall(pattern, ingredients_part)
    
    # Clean up ingredient names (remove potential plural 's' and extra spaces)
    ingredients = [match.rstrip('s ').strip() for match in matches]
    return ingredients if ingredients else None

# Main function that calls for a complex search for recipes from Spoonacular API
def search_complex_recipe(apiKey=api_key, number_of_results=6, force_ingredients=None, query=None, 
                           diet=None, cuisine=None, excludeCuisine=None, intolerances=None, 
                           equipment=None, excludeIngredients=None, type=None, 
                           addRecipeNutrition=False, tags=None):
    """
    Perform a complex search to find recipes based on various parameters including ingredients,
    dietary restrictions, cuisine preferences, and more.
    
    Parameters:
    - api_key: Spoonacular API key.
    - ingredients: (Optional) List of ingredients.
    - number_of_results: The number of recipe results to return.
    - query: (Optional) Natural search query.
    - diet: (Optional) Diet preference.
    - cuisine: (Optional) Cuisine preference.
    - excludeCuisine: (Optional) Exclude cuisine from the search.
    - intolerances: (Optional) Comma-separated list of intolerances.
    - equipment: (Optional) Multiple variables interpreted as 'or'.
    - excludeIngredients: (Optional) Comma-separated list of ingredients to exclude.
    - type: (Optional) Type of the recipe (e.g., main course, dessert).
    - addRecipeNutrition: (Optional) Boolean to include nutrition information.
    - tags: (Optional) Additional tags for the search.
    
    Returns:
    - A list of recipes with detailed information.
    """
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": apiKey,
        "number": number_of_results,
        "addRecipeInformation": True,  # Include detailed recipe information
        "fillIngredients": True,  # Include used and missing ingredients
        "instructionsRequired": True,  # Ensure recipes have instructions
    }
    # print("API: " + api_key)
    # print(url)
    # print(params)
    # Optional parameters
    if force_ingredients:
        params["includeIngredients"] = ','.join(force_ingredients)
    if query:
        params["query"] = query
    if diet:
        params["diet"] = ','.join(diet)
    if cuisine:
        params["cuisine"] = ','.join(cuisine)
    if excludeCuisine:
        params["excludeCuisine"] = ','.join(excludeCuisine)
    if intolerances:
        params["intolerances"] = ','.join(intolerances)
    if equipment:
        params["equipment"] = ','.join(equipment)
    if excludeIngredients:
        params["excludeIngredients"] = ','.join(excludeIngredients)
    if type:
        params["type"] = type
    if addRecipeNutrition:
        params["addRecipeNutrition"] = addRecipeNutrition
    if tags:
        params["tags"] = tags

    # print(url)
    
    response = requests.get(url, params=params)
    # print("Response: ")
    # print(response.status_code)
    # print(response)
    if response.status_code == 200:
        recipes_data = response.json()["results"]
        # recipes_data = response.json()
        # print("recipes_data: ")
        # print(recipes_data)
        recipes = []
        for recipe in recipes_data:
            recipes.append({
                "title": recipe["title"],
                "ingredients": [ingredient["name"] for ingredient in recipe.get("missedIngredients", [])] + [ingredient["name"] for ingredient in recipe.get("usedIngredients", [])],
                "includedIngredients": [ingredient["name"] for ingredient in recipe.get("usedIngredients", [])],
                "excludedIngredients": [ingredient["name"] for ingredient in recipe.get("missedIngredients", [])],
                "steps": [step["step"] for step in recipe["analyzedInstructions"][0]["steps"]] if recipe["analyzedInstructions"] else [],
                "servings": recipe["servings"],
                "time": recipe["readyInMinutes"],
                "image": recipe["image"],
                "nutrition": recipe.get("nutrition", {}).get("nutrients", []) if addRecipeNutrition else None,
                "diet": recipe["diets"],
                "cuisine": recipe["cuisines"],
                "dishTypes": recipe["dishTypes"],
                "intolerances": intolerances,
                "author": recipe["creditsText"],
                "description": recipe["summary"],
            })
        # print(recipes)
        return recipes if recipes else None
    else:
        return f"Error: {response.status_code}"


def process_command(text):
    # Process the text
    doc = nlp(text)

    # Track whether 'allergic' has been encountered
    # past_allergic = False

    # Initialize lists to hold extracted information
    params = {}
    ingredients_to_include = []
    ingredients_to_exclude = []
    extracted_cuisines = []
    extracted_meal_types = []
    extracted_diets = []
    extracted_intolerances = []

    # Flags to determine context based on exclusion keywords
    exclude_context = False

    # Iterate over tokens
    for token in doc:
        word = token.text
        if not word.strip():
            pass
        else:
            word = p.singular_noun(word) or word
        lower_word = word.lower()

        # Check if current token indicates an exclusion or allergy context
        if lower_word in exclusion_keywords:
            exclude_context = True
            continue

        # Check against predefined lists and classify ingredients
        if word in cuisines_list:
            extracted_cuisines.append(word)
        elif word in intolerances_list:
            extracted_intolerances.append(word)
        elif lower_word in meal_types_list:
            extracted_meal_types.append(lower_word)
        elif word in diets_list:
            extracted_diets.append(word)
        elif word in singular_ingredients:  # Check if the word is in the ingredients list
            if exclude_context:
                # Further check if it's a known allergen
                if word in intolerances_list:
                    ingredients_to_exclude.append(word)  # Treat as a specific intolerance/allergen
                else:
                    ingredients_to_exclude.append(word)  # General exclusion
            else:
                ingredients_to_include.append(word)

    if ingredients_to_include:
        params["query"] = ','.join(ingredients_to_include)
    if extracted_diets:
        params["diet"] = ','.join(extracted_diets)
    if extracted_cuisines:
        params["cuisine"] = extracted_cuisines[0]
    if ingredients_to_exclude:
        params["excludeIngredients"] = ','.join(ingredients_to_exclude)
    if extracted_meal_types:
        params["type"] = extracted_meal_types[0]
    
    print("Cuisines:", extracted_cuisines)
    print("Meal Types:", extracted_meal_types)
    print("Diets:", extracted_diets)
    print("Ingredients to Include:", ingredients_to_include)
    print("Ingredients to Exclude:", ingredients_to_exclude)
    
    return params, ingredients_to_include if ingredients_to_include else None