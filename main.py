import spacy
import os

# Load model from local directory
model_path = os.path.join(os.path.dirname(__file__), "en_core_web_sm")

try:
    nlp = spacy.load(model_path)
    print("SpaCy model loaded successfully from local directory!")
except Exception as e:
    print(f"Error loading model: {e}")
