import os
import joblib
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')

# Chargement du modèle entraîné
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Model file not found at {MODEL_PATH}.")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

app = FastAPI(
    title="Iris Prediction API",
    description="A simple API to predict Iris species based on sepal and petal measurements.",
    version="1.0.0",
)


# modèle de données pour la requête d'entrée
class IrisFeatures(BaseModel):
    petal_length: float
    petal_width: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                }
            ]
        }
    }


# endpoint de prédiction
@app.post("/predict")
def predict(features: IrisFeatures):
    try:
        input_features = np.array([
            features.petal_length,
            features.petal_width
        ]).reshape(1, -1)

        prediction = model.predict(input_features)
        prediction_proba = model.predict_proba(input_features)

        return {
            "prediction": int(prediction[0]),
            "prediction_proba": prediction_proba.tolist()[0]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")


@app.get("/health")
def health():
    """Endpoint de santé pour vérifier si l'API est opérationnelle."""
    return {"status": "ok"}
