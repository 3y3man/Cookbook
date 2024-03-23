# Import libraries
import re
import requests

api_key = "d6bb3784b92440028ff33bee93a5b58c"

# API call that finds meals by ingredients
def find_recipes_by_ingredients(api_key, ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": api_key,
        "ingredients": ingredients,  # Comma-separated string of ingredients
        "number": 5  # Adjust the number as needed
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipes = response.json()
        return [(recipe["id"], recipe["title"]) for recipe in recipes]
    else:
        return f"Error: {response.status_code}"


# API call that gets information (recipe, ingridients, servings, etc) about each meal
def get_recipe_information(api_key, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipe_info = response.json()
        ingredients = [ingredient["original"] for ingredient in recipe_info["extendedIngredients"]]
        steps = [step["step"] for step in recipe_info["analyzedInstructions"][0]["steps"]]
        servings = recipe_info["servings"]
        time = recipe_info["readyInMinutes"]
        image = recipe_info["image"]
        return {
            "title": recipe_info["title"],
            "ingredients": ingredients,
            "steps": steps,
            "servings": servings,
            "time": time,
            "image": image,
        }
    else:
        return f"Error: {response.status_code}"


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


# Main function that takes ingredients and gets all recipes you can use them for
def get_full_recipe(ingredients):
    all_recipes = []
    # ingridients_list = extract_ingredient_names(output)
    recipes = find_recipes_by_ingredients(api_key, ", ".join(ingredients))
    # print("Recipes found:", recipes)

    # Get detailed information for the first recipe
    if recipes:
        for recipe in recipes:
            recipe_id = recipe[0]  # Assuming you want the first recipe
            detailed_info = get_recipe_information(api_key, recipe_id)
            all_recipes.append(detailed_info)
            # print(
            #     f"Title: {detailed_info['title']}\nIngredients: {detailed_info['ingredients']}\nSteps: {detailed_info['steps']}\n"
            # )
    return all_recipes