import spacy
import subprocess

model_name = "en_core_web_sm"

# Function to install the model
def install_spacy_model(model_name):
    print(f"Checking if {model_name} is installed...")
    try:
        nlp = spacy.load(model_name)
        print(f"{model_name} is already installed.")
    except OSError:
        print(f"{model_name} not found. Downloading...")
        subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
        print(f"{model_name} installed successfully.")

install_spacy_model(model_name)

# Load the model
nlp = spacy.load(model_name)
print("SpaCy model loaded successfully!")
