# Import libraries
import os
import re
import requests
import subprocess

from keys import Global_Variables
from ultralytics import YOLO

# Setup model and image
globalVar = Global_Variables()
# image_path = "static/foods1.jpg"
best_model = globalVar.obj_model
# Global variables api_key
api_key = globalVar.RECIPE_API
# print(api_key)

# function to run a cli prediction on a given image
def identifier(img):
      # CLI for inference
      cmd = f"yolo task=detect mode=predict model={best_model} conf=0.25 source={img} save=False"

      # Run the inference command and capture the output
      result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
      
      return result.stderr


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
    return ingredients

# Main function that calls for a complex search for recipes from Spoonacular API
def search_complex_recipe(number_of_results=5, ingredients=None, query=None, 
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
        "apiKey": api_key,
        "number": number_of_results,
        "addRecipeInformation": True,  # Include detailed recipe information
        "fillIngredients": True,  # Include used and missing ingredients
        "instructionsRequired": True,  # Ensure recipes have instructions
    }

    # Optional parameters
    if ingredients:
        params["includeIngredients"] = '|'.join(ingredients)
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

    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipes_data = response.json()["results"]
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
            })
        return recipes
    else:
        return f"Error: {response.status_code}"


# request = search_recipes_complex(api_key, cuisine=['African'])
# for recipe in request:
#     print(recipe)