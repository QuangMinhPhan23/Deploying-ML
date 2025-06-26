import requests
import json
import argparse

def test_prediction(url="http://127.0.0.1:8888"):
    """
    Test the prediction API with sample data
    """
    # Sample data for an extrovert personality using the detailed format
    extrovert_data = {
        "time_spent_alone": 2,
        "stage_fear": False,
        "social_event_attendance": 8,
        "going_outside": 5,
        "drained_after_socializing": False,
        "friends_circle_size": 15,
        "post_frequency": 10
    }

    # Sample data for an introvert personality using the detailed format
    introvert_data = {
        "time_spent_alone": 8,
        "stage_fear": True,
        "social_event_attendance": 2,
        "going_outside": 2,
        "drained_after_socializing": True,
        "friends_circle_size": 3,
        "post_frequency": 1
    }

    # Make prediction requests
    prediction_url = f"{url}/predict"
    
    print("Testing with extrovert-like features...")
    extrovert_response = requests.post(
        prediction_url, 
        json=extrovert_data
    )
    
    print("Testing with introvert-like features...")
    introvert_response = requests.post(
        prediction_url, 
        json=introvert_data
    )
    
    # Display results
    print("\n=== API Test Results ===\n")
    
    if extrovert_response.status_code == 200:
        extrovert_result = extrovert_response.json()
        print(f"Extrovert Test: {json.dumps(extrovert_result, indent=2)}")
    else:
        print(f"Extrovert Test Failed: {extrovert_response.status_code}")
        print(extrovert_response.text)
    
    print("\n---\n")
    
    if introvert_response.status_code == 200:
        introvert_result = introvert_response.json()
        print(f"Introvert Test: {json.dumps(introvert_result, indent=2)}")
    else:
        print(f"Introvert Test Failed: {introvert_response.status_code}")
        print(introvert_response.text)

def test_feedback(url="http://127.0.0.1:8888", prediction_id=1):
    """
    Test the feedback API
    """
    feedback_data = {
        "prediction_id": prediction_id,
        "feedback": "correct"
    }
    
    feedback_url = f"{url}/feedback"
    
    print("\nSubmitting test feedback...")
    response = requests.post(feedback_url, json=feedback_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Feedback Test: {json.dumps(result, indent=2)}")
    else:
        print(f"Feedback Test Failed: {response.status_code}")
        print(response.text)

def test_history(url="http://127.0.0.1:8888", limit=5):
    """
    Test the history API
    """
    history_url = f"{url}/history?limit={limit}"
    
    print("\nFetching prediction history...")
    response = requests.get(history_url)
    
    if response.status_code == 200:
        results = response.json()
        print(f"History Test: Found {len(results)} records")
        if results:
            print("Sample record:")
            print(json.dumps(results[0], indent=2))
    else:
        print(f"History Test Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Personality Prediction API")
    parser.add_argument("--url", default="http://127.0.0.1:8888", help="API base URL")
    parser.add_argument("--test", choices=["prediction", "feedback", "history", "all"], default="all", 
                        help="Which test to run")
    parser.add_argument("--prediction-id", type=int, default=1, help="Prediction ID for feedback test")
    parser.add_argument("--limit", type=int, default=5, help="Limit for history test")
    
    args = parser.parse_args()
    
    if args.test == "prediction" or args.test == "all":
        test_prediction(args.url)
    
    if args.test == "feedback" or args.test == "all":
        test_feedback(args.url, args.prediction_id)
    
    if args.test == "history" or args.test == "all":
        test_history(args.url, args.limit)