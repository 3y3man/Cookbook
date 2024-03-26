import unittest
import requests_mock
from helpers import identifier, extract_ingredient_names, search_complex_recipe

class TestHelpers(unittest.TestCase):
    
    def test_identifier(self):
        """Test the identifier function with a mock image path."""
        # Assuming the identifier function is supposed to return a specific format of string.
        # Here, you'll need to mock the subprocess call within the identifier and assert its return value.
        img_path = "mock_image.jpg"
        expected_output = "Ultralytics YOLOv8.0.196  Python-3.11.4 torch-2.2.0+cpu CPU (Intel Core(TM) i7-8850H 2.60GHz)\nModel summary (fused): 168 layers, 11130615 parameters, 0 gradients, 28.5 GFLOPs\n\nimage 1/1 c:\\Users\\HP\\Documents\\PlayGround\\Capstone_AI-Recipe_Recomendation\\ChefGPT main\\static\\foods1.jpg: 544x800 4 carrots, 2 cucumbers, 1 eggplant, 2 white radishs, 421.5ms\nSpeed: 15.6ms preprocess, 421.5ms inference, 15.6ms postprocess per image at shape (1, 3, 544, 800)\n Learn more at https://docs.ultralytics.com/modes/predict\n"  # This should be replaced with an expected output format
        self.assertEqual(identifier(img_path), expected_output)
    
    def test_extract_ingredient_names(self):
        """Test the extract_ingredient_names function."""
        yolov8_output = "Ultralytics YOLOv8.0.196  Python-3.11.4 torch-2.2.0+cpu CPU (Intel Core(TM) i7-8850H 2.60GHz)\nModel summary (fused): 168 layers, 11130615 parameters, 0 gradients, 28.5 GFLOPs\n\nimage 1/1 c:\\Users\\HP\\Documents\\PlayGround\\Capstone_AI-Recipe_Recomendation\\ChefGPT main\\static\\foods1.jpg: 544x800 4 carrots, 2 cucumbers, 1 eggplant, 2 white radishs, 421.5ms\nSpeed: 15.6ms preprocess, 421.5ms inference, 15.6ms postprocess per image at shape (1, 3, 544, 800)\n Learn more at https://docs.ultralytics.com/modes/predict\n"
        expected_ingredients = ['carrot', 'cucumber', 'eggplant', 'white radish']
        self.assertEqual(extract_ingredient_names(yolov8_output), expected_ingredients)

    @requests_mock.Mocker()
    def test_search_complex_recipe(self, m):
        """Test the search_complex_recipe function with a mock API response."""
        mock_response = {
            "results": [
                {"title": "Mock Recipe", "servings": 4, "readyInMinutes": 45, "image": "mock_image.jpg"}
            ]
        }
        m.get("https://api.spoonacular.com/recipes/complexSearch", json=mock_response)

        ingredients = ['carrot', 'cucumber', 'eggplant', 'white radish']
        recipes = search_complex_recipe(force_ingredients=ingredients)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]['title'], "Mock Recipe")

if __name__ == '__main__':
    unittest.main()
