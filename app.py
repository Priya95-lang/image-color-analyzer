from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"})
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"})

    try:
        img = Image.open(file).convert("RGB")
        img = img.resize((100, 100))
        arr = np.array(img)
        avg_color = arr.reshape(-1, 3).mean(axis=0).astype(int)
        r, g, b = avg_color
        hex_color = '#%02x%02x%02x' % (r, g, b)

        return jsonify({
            "r": int(r),
            "g": int(g),
            "b": int(b),
            "hex": hex_color
        })
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "False") == "True")
