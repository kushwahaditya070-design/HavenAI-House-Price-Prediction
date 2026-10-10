from flask import Flask, render_template, request, jsonify
from pathlib import Path
import pickle
import numpy as np

app = Flask(__name__)
MODEL_PATH = Path(__file__).parent / "model" / "HP_LR_model.pkl"

# IMPORTANT:
# The uploaded pickle contains a 4-input LinearRegression model, but does not
# store the original feature names. Replace these labels with your training
# feature names in the EXACT order used when fitting the model.
FEATURES = [
    {"key": "house_size", "label": "House Size", "placeholder": "e.g. 1800", "unit": "sq ft", "step": "0.01", "min": 0},
    {"key": "bedrooms", "label": "Number of Bedrooms", "placeholder": "e.g. 3", "unit": "bedrooms", "step": "1", "min": 0},
    {"key": "bathrooms", "label": "Number of Bathrooms", "placeholder": "e.g. 2", "unit": "bathrooms", "step": "1", "min": 0},
    {"key": "floors", "label": "Number of Floors", "placeholder": "e.g. 2", "unit": "floors", "step": "1", "min": 1},
]

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    MODEL_ERROR = None
except Exception as exc:
    model = None
    MODEL_ERROR = str(exc)

EXPECTED_FEATURES = getattr(model, "n_features_in_", 4) if model is not None else 4

@app.get("/")
def home():
    return render_template("index.html", features=FEATURES)

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok" if model is not None else "error",
        "model_loaded": model is not None,
        "feature_count": EXPECTED_FEATURES,
        "feature_names_configured": all(not f["label"].startswith("Feature ") for f in FEATURES),
        "error": MODEL_ERROR
    })

@app.post("/api/predict")
def predict():
    if model is None:
        return jsonify({"error": "Model could not be loaded.", "details": MODEL_ERROR}), 500
    data = request.get_json(silent=True) or {}
    values = []
    try:
        for feature in FEATURES:
            raw = data.get(feature["key"])
            if raw is None or str(raw).strip() == "":
                return jsonify({"error": f'Please enter {feature["label"]}.'}), 400
            value = float(raw)
            if not np.isfinite(value):
                raise ValueError
            if feature["min"] is not None and value < float(feature["min"]):
                return jsonify({"error": f'{feature["label"]} must be at least {feature["min"]}.'}), 400
            if feature["key"] in {"bedrooms", "bathrooms", "floors"} and not value.is_integer():
                return jsonify({"error": f'{feature["label"]} must be a whole number.'}), 400
            values.append(value)

        if len(values) != EXPECTED_FEATURES:
            return jsonify({"error": f"Model expects {EXPECTED_FEATURES} inputs but the form is configured for {len(values)}."}), 500

        result = float(model.predict(np.array([values], dtype=float))[0])
        return jsonify({"prediction": result, "inputs": dict(zip([f["key"] for f in FEATURES], values))})
    except ValueError:
        return jsonify({"error": "Please enter valid numeric values in all fields."}), 400
    except Exception as exc:
        return jsonify({"error": "Prediction failed.", "details": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
