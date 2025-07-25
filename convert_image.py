import os
from tkinter import Tk, filedialog
from PIL import Image

# Hide main tkinter window
root = Tk()
root.withdraw()

# Ask user to select an image file
file_path = filedialog.askopenfilename(
    title="Select an image",
    filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
)

if not file_path:
    print("No file selected.")
    exit()

# Resize the image to 640x480
with Image.open(file_path) as img:
    resized_img = img.resize((640, 480), Image.Resampling.LANCZOS)

# Ensure /resources directory exists
output_dir = os.path.join(os.path.dirname(__file__), "resources")
os.makedirs(output_dir, exist_ok=True)

# Auto-increment filename like image_1.jpg
def get_next_filename(directory, prefix="image_", extension=".jpg"):
    i = 1
    while True:
        filename = f"{prefix}{i}{extension}"
        full_path = os.path.join(directory, filename)
        if not os.path.exists(full_path):
            return full_path
        i += 1

# Get next available filename
ext = os.path.splitext(file_path)[1].lower() or ".jpg"
output_path = get_next_filename(output_dir, prefix="image_", extension=ext)

# Save the resized image
resized_img.save(output_path)
print(f"Image saved to {output_path}")