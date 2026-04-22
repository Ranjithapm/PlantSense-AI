from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import cv2
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ── PlantVillage 15-class labels (matched from class_indices.json) ─────────────
CLASSES = {
    0:  {'name': 'Pepper – Bacterial Spot',              'type': 'Disease', 'remedy': 'Use disease-free seeds. Apply copper-based bactericides. Avoid overhead irrigation.'},
    1:  {'name': 'Pepper – Healthy',                     'type': 'Healthy', 'remedy': 'No action needed. Continue regular care and monitoring.'},
    2:  {'name': 'Potato – Early Blight',                'type': 'Disease', 'remedy': 'Apply chlorothalonil or mancozeb fungicide. Avoid overhead irrigation. Remove infected leaves.'},
    3:  {'name': 'Potato – Late Blight',                 'type': 'Disease', 'remedy': 'Apply metalaxyl-based fungicides immediately. Destroy infected plants to stop spread.'},
    4:  {'name': 'Potato – Healthy',                     'type': 'Healthy', 'remedy': 'No action needed. Continue regular care and monitoring.'},
    5:  {'name': 'Tomato – Bacterial Spot',              'type': 'Disease', 'remedy': 'Apply copper-based bactericides. Use resistant varieties. Avoid working with wet plants.'},
    6:  {'name': 'Tomato – Early Blight',                'type': 'Disease', 'remedy': 'Apply mancozeb or chlorothalonil. Remove lower infected leaves. Rotate crops.'},
    7:  {'name': 'Tomato – Late Blight',                 'type': 'Disease', 'remedy': 'Apply metalaxyl fungicides. Avoid wet foliage. Remove and destroy infected plants.'},
    8:  {'name': 'Tomato – Leaf Mold',                   'type': 'Disease', 'remedy': 'Reduce humidity in greenhouse. Apply chlorothalonil fungicide. Improve air circulation.'},
    9:  {'name': 'Tomato – Septoria Leaf Spot',          'type': 'Disease', 'remedy': 'Remove infected leaves immediately. Apply mancozeb fungicide. Avoid overhead watering.'},
    10: {'name': 'Tomato – Spider Mites',                'type': 'Pest',    'remedy': 'Apply miticides or neem oil. Increase humidity around plants. Remove heavily infested leaves.'},
    11: {'name': 'Tomato – Target Spot',                 'type': 'Disease', 'remedy': 'Apply fungicides (azoxystrobin). Remove crop debris after harvest. Practice crop rotation.'},
    12: {'name': 'Tomato – Yellow Leaf Curl Virus',      'type': 'Virus',   'remedy': 'Control whitefly vectors. Use reflective mulches. Remove and destroy infected plants.'},
    13: {'name': 'Tomato – Mosaic Virus',                'type': 'Virus',   'remedy': 'Use virus-free seeds. Control aphid vectors. Wash hands before handling plants.'},
    14: {'name': 'Tomato – Healthy',                     'type': 'Healthy', 'remedy': 'No action needed. Continue regular care and monitoring.'},
}

# ── Try loading trained model ─────────────────────────────────────────────────
MODEL_LOADED = False
model = None

try:
    import tensorflow as tf
    model_path = os.path.join('model', 'plant_model.h5')
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        MODEL_LOADED = True
        print("[INFO] Trained model loaded successfully.")
    else:
        print("[WARN] Model file not found. Running in DEMO mode.")
except Exception as e:
    print(f"[WARN] Could not load model: {e}. Running in DEMO mode.")


# ── Multispectral Preprocessing ───────────────────────────────────────────────
def extract_spectral_indices(image_path):
    """Compute vegetation indices and return spectral stats."""
    img_bgr = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    R = img_rgb[:, :, 0].astype(float)
    G = img_rgb[:, :, 1].astype(float)
    B = img_rgb[:, :, 2].astype(float)
    eps = 1e-10

    ExG  = float(np.mean(2 * G - R - B))
    ExR  = float(np.mean(1.4 * R - G))
    VARI = float(np.mean(np.clip((G - R) / (G + R - B + eps), -1, 1)))
    greenness = float(np.mean(G) / (np.mean(R) + np.mean(G) + np.mean(B) + eps) * 100)

    # Clamp to readable display range
    def pct(v, lo, hi): return round((v - lo) / (hi - lo + eps) * 100, 1)

    return {
        'ExG':       round(pct(ExG,  -255, 510), 1),
        'ExR':       round(pct(ExR,  -255, 357), 1),
        'VARI':      round((VARI + 1) / 2 * 100, 1),
        'greenness': round(max(0, min(100, greenness)), 1),
    }


def preprocess_for_model(image_path, target_size=(224, 224)):
    """Return normalised numpy array ready for MobileNetV2 input."""
    img_bgr = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, target_size)
    img_normalised = img_resized.astype(np.float32) / 255.0
    return np.expand_dims(img_normalised, axis=0)


def is_plant_image(image_path, threshold=0.06):
    """Check if image contains a plant/leaf using green pixel ratio in HSV."""
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        return False, 0.0
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # Green hue range in HSV: 35-85 degrees
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(img_hsv, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / mask.size
    return green_ratio >= threshold, round(green_ratio * 100, 1)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({'status': 'ok', 'model_loaded': MODEL_LOADED})

@app.route('/status')
def status():
    return jsonify({'model_loaded': MODEL_LOADED})


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save file
    ext = os.path.splitext(file.filename)[1] or '.jpg'
    filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # ── Plant Detection Check ────────────────────────────────────────────────
    is_plant, green_score = is_plant_image(filepath)
    if not is_plant:
        return jsonify({
            'error': f'Invalid Image: No plant detected (Greenness: {green_score}%). Please upload a clear photo of a plant leaf.'
        }), 400

    # ── Predictions ──────────────────────────────────────────────────────────
    if MODEL_LOADED and model is not None:
        img_input = preprocess_for_model(filepath)
        preds = model.predict(img_input)[0]
        top3 = preds.argsort()[-3:][::-1]
        results = [
            {
                'class_id':   int(i),
                'name':       CLASSES[i]['name'],
                'type':       CLASSES[i]['type'],
                'remedy':     CLASSES[i]['remedy'],
                'confidence': round(float(preds[i]) * 100, 2),
            }
            for i in top3
        ]
    else:
        # ── DEMO MODE: simulated results ─────────────────────────────────────
        demo_picks = random.sample(list(CLASSES.keys()), 3)
        confs = sorted([random.uniform(65, 94), random.uniform(3, 20), random.uniform(0.5, 5)], reverse=True)
        results = [
            {
                'class_id':   demo_picks[i],
                'name':       CLASSES[demo_picks[i]]['name'],
                'type':       CLASSES[demo_picks[i]]['type'],
                'remedy':     CLASSES[demo_picks[i]]['remedy'],
                'confidence': round(confs[i], 2),
            }
            for i in range(3)
        ]

    spectral = extract_spectral_indices(filepath)

    return jsonify({
        'success':    True,
        'predictions': results,
        'spectral':   spectral,
        'image_url':  f'/static/uploads/{filename}',
        'demo_mode':  not MODEL_LOADED,
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
