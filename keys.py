class Global_Variables:
    def __init__(self):
        self._RECIPE_API = "d6bb3784b92440028ff33bee93a5b58c"  # Spoonacular API
        # self._obj_model = "models/yolo_best_model_1.pt"
        self._obj_model = "models/best.pt"

    @property
    def RECIPE_API(self):
        """Getter method for the Spoonacular API."""
        return self._RECIPE_API
    
    @property
    def obj_model(self):
        """Getter method for the current ingredients detection model version."""
        return self._obj_model
