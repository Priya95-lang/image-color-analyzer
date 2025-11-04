from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import os
#venv\Scripts\activate

app = Flask(__name__)

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

    img = Image.open(file).convert("RGB")
    img = img.resize((100, 100))  # speed up
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

if __name__ == "__main__":
    app.run(debug=True)
