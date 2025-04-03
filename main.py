import spacy
import os

# Get the full model path
model_path = os.path.join(os.path.dirname(spacy.__file__), "data", "en_core_web_sm")

print(f"🔍 Looking for model at: {model_path}")  # Debug print

try:
    nlp = spacy.load("en_core_web_sm")  # Load directly if installed in environment
    print("✅ SpaCy model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
