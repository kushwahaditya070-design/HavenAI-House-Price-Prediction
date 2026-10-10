# HP LR Housing Predictor

A responsive HTML/CSS/JavaScript frontend with a Flask prediction API and your uploaded `HP_LR_model.pkl`.

## Important: configure the actual feature names

The pickle contains a scikit-learn `LinearRegression` model with **4 numeric inputs**. The frontend is configured in this order, as confirmed by the user:
1. House Size (sq ft)
2. Number of Bedrooms
3. Number of Bathrooms
4. Number of Floors

Keep this order consistent with the model's training order.

## Run on Windows

Open PowerShell in this folder and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## API

- `GET /api/health` — checks whether the model loaded and reports the input count.
- `POST /api/predict` — accepts JSON with `house_size`, `bedrooms`, `bathrooms`, and `floors`.

Example request body (replace values with valid inputs for your model):

```json
{
  "house_size": 1800,
  "bedrooms": 3,
  "bathrooms": 2,
  "floors": 2
}
```

The model was saved with scikit-learn 1.6.1, so that version is pinned in `requirements.txt`.
