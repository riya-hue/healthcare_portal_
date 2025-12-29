from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from fastapi.staticfiles import StaticFiles
from sklearn.ensemble import RandomForestClassifier

app = FastAPI(title="Heart Disease Prediction API")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    [58,0,3,150,283,1,0,162,0,1.0,2,0,2],
    [50,1,2,140,233,0,1,163,0,0.6,2,1,3],
    [52,1,0,128,204,1,1,156,1,1.0,1,0,3],
    [44,1,1,120,263,0,1,173,0,0.0,2,0,2],
    [61,0,3,145,307,0,0,146,1,1.0,1,0,3],
    [60,1,0,130,253,0,1,144,1,1.4,1,1,3],
    [55,0,1,135,250,0,0,161,0,1.2,2,0,2],
    [46,1,2,120,249,0,1,144,0,0.8,2,0,2],
    [39,0,2,94,199,0,1,179,0,0.0,2,0,2],
    [59,1,3,160,273,0,0,125,1,0.0,1,2,3],
    [47,1,1,138,257,0,0,156,0,0.0,2,0,2],
    [51,0,0,140,299,0,1,173,1,1.6,2,0,3],
    [62,1,3,120,267,0,1,99,1,1.8,1,2,3],
    [43,0,1,122,213,0,1,165,0,0.2,2,0,2],
    [54,1,2,108,309,0,1,156,0,0.0,2,0,2],
    [65,1,0,135,269,0,1,114,1,1.2,1,1,3],
    [42,0,2,120,295,0,1,162,0,0.0,2,0,2],
    [58,1,0,140,207,0,0,138,1,0.8,1,1,3],
    [49,0,1,134,271,0,1,162,0,0.0,2,0,2],
    [53,1,2,130,246,1,0,173,0,0.0,2,0,2],
])

y = np.array([
    1,1,1,1,0,0,1,0,0,1,
    0,1,1,0,1,1,0,0,0,1,
    0,1,1,0,0,1,0,1,0,0
])  # 1 = Heart Disease, 0 = No Disease


model = RandomForestClassifier(
    n_estimators=40,
    max_depth=6,
    random_state=42
)
model.fit(X, y)

# -------------------------------------------------
# Request Body
# -------------------------------------------------

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


@app.get("/")
def home():
    return {"status": "Heart Disease API running"}

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

