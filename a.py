import os

font_path = "fonts/DejaVuSans.ttf"  # Adjust if needed
if not os.path.exists(font_path):
    print(f"Font file not found: {font_path}")
else:
    print("Font file exists.")
