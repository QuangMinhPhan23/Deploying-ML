# Personality Prediction Web App

A complete web application for personality prediction (Extrovert/Introvert) with React frontend, FastAPI backend, and database storage.

## Features

- **Interactive Quiz**: Answer questions about your behavior and preferences
- **ML-Powered Predictions**: Get predictions based on a trained machine learning model
- **User Feedback**: Provide feedback on prediction accuracy
- **Data Storage**: All predictions and feedback are stored in a database
- **Modern UI**: Clean, responsive user interface built with React and Bootstrap

## Docker Instructions

### Building the Container
```
docker build -t personality-prediction-app .
```

### Running the Container
```
docker run -p 8888:8888 personality-prediction-app
```

### Accessing the Application
When running with Docker, access the application at:
```
http://localhost:8888
```

⚠️ **IMPORTANT:** 
- Do NOT try to use http://0.0.0.0:8888 in your browser
- The 0.0.0.0 address shown in Docker logs is only for internal container configuration
- Always use localhost:8888 instead

## Local Development

### Backend Setup

1. Install Python dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python run.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install Node.js dependencies:
```
npm install
```

3. Start the development server:
```
npm start
```

The frontend development server will run at http://localhost:3000

## API Endpoints

- `/` - Web application (when built) or welcome page
- `/docs` - Interactive Swagger documentation
- `/predict` - Make personality predictions (POST)
- `/feedback` - Submit feedback on predictions (POST)
- `/history` - Get prediction history (GET)

## Cloud Deployment Options

### Heroku Deployment

1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku:
```
heroku login
```

3. Create a new Heroku app:
```
heroku create personality-prediction-app
```

4. Set the stack to container:
```
heroku stack:set container
```

5. Push to Heroku:
```
git push heroku main
```

### Other Cloud Options

This application can also be deployed on:
- AWS (EC2, ECS, Elastic Beanstalk)
- Azure (App Service, AKS)
- Google Cloud (GKE, App Engine)

## Database

The application uses SQLite for data storage. The database file `personality_predictions.db` is created automatically when the application runs for the first time.
<img width="1504" height="712" alt="image" src="https://github.com/user-attachments/assets/45a06931-d7eb-4aa4-b890-3ea5b2161d14" />


