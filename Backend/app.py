from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Enable CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
logistic_model = joblib.load("models/logistic_model.joblib")
tree_model = joblib.load("models/decision_tree_model.joblib")

# Feature names
FEATURE_NAMES = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
    'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
    'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
    'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst',
    'symmetry_worst', 'fractal_dimension_worst'
]

# Pydantic model for input
class InputData(BaseModel):
    features: list[float]  # Must contain exactly 30 values

@app.get("/")
def root():
    return {"message": "API is working"}

@app.post("/predict")
def predict(data: InputData, model_type: str = Query("logistic", description="Choose model: 'logistic' or 'tree'")):
    """
    Predict breast cancer using either logistic regression or decision tree model.
    model_type: "logistic" or "tree"
    """
    if len(data.features) != 30:
        return {"error": "Exactly 30 features are required."}

    # Convert list to DataFrame with correct column names
    df = pd.DataFrame([data.features], columns=FEATURE_NAMES)

    # Choose model
    if model_type.lower() == "tree":
        prediction = tree_model.predict(df)
    else:
        prediction = logistic_model.predict(df)

    return {"prediction": int(prediction[0]), "model_used": model_type.lower()}
