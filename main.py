import spacy
import subprocess

# Ensure model is installed
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ SpaCy model loaded successfully!")
except OSError:
    print("⚠️ Model not found, installing now...")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")
    print("✅ SpaCy model installed and loaded!")
