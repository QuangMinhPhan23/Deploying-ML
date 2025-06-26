from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pickle
import numpy as np
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, Float, String, ARRAY, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import json

# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
    
class_names = ['Extrovert', 'Introvert']

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./personality_predictions.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionRecord(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    features = Column(String)  # Store as JSON string
    predicted_class = Column(String)
    extrovert_probability = Column(Float)
    introvert_probability = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_feedback = Column(String, nullable=True)
    
    # Helper properties for easier access to structured feature data
    @property
    def feature_details(self):
        try:
            return json.loads(self.features)
        except:
            return None

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI(
    title="Personality Prediction API",
    description="API for predicting personality type (Extrovert/Introvert)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin for Render deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class FeatureInput(BaseModel):
    features: List[float] = None  # Keeping for backward compatibility
    
    # New specific input fields
    time_spent_alone: Optional[int] = None
    stage_fear: Optional[bool] = None
    social_event_attendance: Optional[int] = None
    going_outside: Optional[int] = None
    drained_after_socializing: Optional[bool] = None
    friends_circle_size: Optional[int] = None
    post_frequency: Optional[int] = None
    
    user_id: Optional[str] = None

class FeedbackInput(BaseModel):
    prediction_id: int
    feedback: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mount static files from the React build
if os.path.exists("./static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    # If we have the React build, serve the index.html
    if os.path.exists("./static/index.html"):
        return FileResponse("./static/index.html")
    return {"message": "Welcome to the Personality Prediction API!"}

# API routes for spa frontend
@app.get("/api")
def api_root():
    return {"message": "Welcome to the Personality Prediction API!"}

# Keep the original predict endpoint for compatibility
@app.post("/predict")
def predict(input_data: FeatureInput, db: Session = Depends(get_db)):
    # Check if we're using the new detailed format or the old list format
    if input_data.features is not None:
        features = input_data.features
    else:
        # Convert the detailed input to features list
        features = [
            input_data.time_spent_alone if input_data.time_spent_alone is not None else 0,
            1 if input_data.stage_fear else 0,
            input_data.social_event_attendance if input_data.social_event_attendance is not None else 0,
            input_data.going_outside if input_data.going_outside is not None else 0,
            1 if input_data.drained_after_socializing else 0,
            input_data.friends_circle_size if input_data.friends_circle_size is not None else 0,
            input_data.post_frequency if input_data.post_frequency is not None else 0
        ]
    
    # Ensure the input is a valid list of numerical features
    if not isinstance(features, list) or not all(isinstance(i, (int, float)) for i in features):
        raise HTTPException(status_code=400, detail="Invalid input format. Please provide a list of numerical features.")
    
    # Reshape the input to match the model's expected input shape
    features_array = np.array(features).reshape(1, -1)
    
    # Make prediction
    predicted_class = model.predict(features_array)[0]
    predicted_prob = model.predict_proba(features_array)[0]
    
    # Save to database with detailed information
    feature_detail = {
        "time_spent_alone": input_data.time_spent_alone if input_data.time_spent_alone is not None else features[0],
        "stage_fear": input_data.stage_fear if input_data.stage_fear is not None else bool(features[1]),
        "social_event_attendance": input_data.social_event_attendance if input_data.social_event_attendance is not None else features[2],
        "going_outside": input_data.going_outside if input_data.going_outside is not None else features[3],
        "drained_after_socializing": input_data.drained_after_socializing if input_data.drained_after_socializing is not None else bool(features[4]),
        "friends_circle_size": input_data.friends_circle_size if input_data.friends_circle_size is not None else features[5],
        "post_frequency": input_data.post_frequency if input_data.post_frequency is not None else features[6]
    }
    
    db_record = PredictionRecord(
        features=json.dumps(feature_detail),
        predicted_class=class_names[predicted_class],
        extrovert_probability=float(predicted_prob[0]),
        introvert_probability=float(predicted_prob[1]),
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return {
        "prediction_id": db_record.id,
        "class": class_names[predicted_class],
        "probability": predicted_prob.tolist(),
        "feature_details": feature_detail
    }

@app.post("/feedback")
def submit_feedback(feedback_data: FeedbackInput, db: Session = Depends(get_db)):
    # Get the prediction record
    db_record = db.query(PredictionRecord).filter(PredictionRecord.id == feedback_data.prediction_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Prediction record not found")
    
    # Update with feedback
    db_record.user_feedback = feedback_data.feedback
    db.commit()
    
    return {"message": "Feedback submitted successfully"}

@app.get("/history")
def get_prediction_history(limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(PredictionRecord).order_by(PredictionRecord.timestamp.desc()).limit(limit).all()
    
    # Format the records with feature details
    formatted_records = []
    for record in records:
        formatted_record = {
            "id": record.id,
            "predicted_class": record.predicted_class,
            "extrovert_probability": record.extrovert_probability,
            "introvert_probability": record.introvert_probability,
            "timestamp": record.timestamp.isoformat(),
            "user_feedback": record.user_feedback
        }
        
        # Add feature details if available
        try:
            formatted_record["feature_details"] = json.loads(record.features)
        except:
            formatted_record["features"] = record.features
            
        formatted_records.append(formatted_record)
        
    return formatted_records
