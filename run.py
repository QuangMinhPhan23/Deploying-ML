import os
import subprocess
import sqlite3

# Check if model.pkl exists, if not, run main.py to create it
if not os.path.exists('model.pkl'):
    print("Model file not found. Training model...")
    subprocess.run(['python', 'main.py'])
    print("Model training complete.")

# Check if the database exists, if not, it will be created when the server starts
db_file = 'personality_predictions.db'
if not os.path.exists(db_file):
    print(f"Database file {db_file} not found. It will be created when the server starts.")

# Run the FastAPI server
print("Starting API server...")
subprocess.run(['uvicorn', 'server:app', '--host', '0.0.0.0', '--port', '8888'])
