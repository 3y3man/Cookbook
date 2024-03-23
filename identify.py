# Import libraries and helper functions
import subprocess
from ultralytics import YOLO
from helpers import get_full_recipe, extract_ingredient_names

# Setup model and image
# image_path = "foods1.jpg"
best_model = "models/yolo_best_model_1.pt"


def identifier(img):
      # CLI for inference
      cmd = f"yolo task=detect mode=predict model={best_model} conf=0.25 source={img} save=False"

      # Run the inference command and capture the output
      result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
      
      return result.stderr

