
---

# Food Recommender Application

## Overview

The Food Recommender Application is an innovative solution designed to transform the way individuals discover recipes and culinary inspirations. Leveraging state-of-the-art image recognition and natural language processing technologies, the app allows users to effortlessly find recipes based on ingredients they have on hand, either through uploading images or using natural language inputs (typed or spoken).

## Features

- **Ingredient Detection**: Utilizes a YOLO model to detect ingredients from user-uploaded images.
- **Natural Language Queries**: Supports typing or speaking natural language queries to search for recipes.
- **Recipe Recommendations**: Recommends recipes based on detected ingredients or processed queries, tailored to user preferences and dietary restrictions.
- **User Interaction**: Enables users to like, comment on, and share their favorite recipes.
- **Responsive UI**: Offers a clean, user-friendly interface for a seamless experience on various devices.

## Getting Started

### Prerequisites

- Python 3.8 or newer
- Flask
- PyTorch or TensorFlow (for YOLO model integration)
- An NLU service or library (e.g., Google Cloud Natural Language API, spaCy)
- A speech-to-text service API key (if implementing voice input)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/3y3man/Cookbook.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables for any external API keys required (e.g., for NLU or speech-to-text services).

### Running the Application

1. Start the Flask server:
   ```
   flask run
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

## Usage

- **Uploading Images**: Click on the upload area or drag and drop an image to detect ingredients.
- **Exploring Recipes**: Browse through the recommended recipes based on your input and discover new culinary ideas.
- **Voice/Text Input**: `Not Connected` Click on the microphone icon to speak or use the text box to type your query. 

## Contributing

We welcome contributions to the Food Recommender Application! If you have suggestions for improvements or bug fixes, please feel free to fork the repository and submit a pull request.

## Acknowledgments

- Special thanks to all the open-source projects and APIs that made this app possible.
- Our community of users and contributors who inspire us to keep improving.

---

Created by Ayman Bukar
Project Start Date: 20th January, 2024