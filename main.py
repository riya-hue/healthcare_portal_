from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = FastAPI(title="Heart Disease Prediction API")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect root to index.html
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# ------------------ MODEL ------------------
X = np.array([
    [63,1,3,145,233,1,0,150,0,2.3,0,0,1],
    [37,1,2,130,250,0,1,187,0,3.5,0,0,2],
    [41,0,1,130,204,0,0,172,0,1.4,2,0,2],
    [56,1,1,120,236,0,1,178,0,0.8,2,0,2],
    [57,0,0,120,354,0,1,163,1,0.6,2,0,2],
    [45,1,3,140,308,0,0,170,0,0.0,2,0,2],
    [54,1,0,124,266,0,0,109,1,2.2,1,1,3],
    [48,0,2,130,275,0,1,139,0,0.2,2,0,2],
    [49,1,1,130,266,0,1,171,0,0.6,2,0,2],
    [64,1,3,110,211,0,0,144,1,1.8,1,0,2],
])

y = np.array([1,1,1,1,0,0,1,0,0,1])

model = RandomForestClassifier(n_estimators=40, max_depth=6, random_state=42)
model.fit(X, y)

# ------------------ REQUEST BODY ------------------
class HeartData(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float

# ------------------ API ------------------
@app.post("/analyze_heart")
def analyze_heart(data: HeartData):
    features = np.array([[ 
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang,
        data.oldpeak, data.slope, data.ca, data.thal
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "heart_disease": "Yes" if prediction == 1 else "No",
        "risk_probability": round(probability * 100, 2)
    }


