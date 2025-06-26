import React, { useState } from 'react';
import { Container, Row, Col, Card, Button, Form, ProgressBar, Badge, Alert, InputGroup } from 'react-bootstrap';
import { predictPersonality, submitFeedback } from './services/api';
import './App.css';

// Define the personality quiz questions with appropriate input types
const personalityQuestions = [
  {
    id: 1,
    text: "How many hours do you typically spend alone in a day?",
    field: "time_spent_alone",
    type: "number",
    min: 0,
    max: 24,
    placeholder: "Hours (0-24)"
  },
  {
    id: 2,
    text: "Do you experience stage fear?",
    field: "stage_fear",
    type: "boolean"
  },
  {
    id: 3,
    text: "How many social events do you attend in a typical month?",
    field: "social_event_attendance",
    type: "number",
    min: 0,
    placeholder: "Number of events"
  },
  {
    id: 4,
    text: "How many days per week do you go outside for social activities?",
    field: "going_outside",
    type: "number",
    min: 0,
    max: 7,
    placeholder: "Days per week (0-7)"
  },
  {
    id: 5,
    text: "Do you feel drained after socializing?",
    field: "drained_after_socializing",
    type: "boolean"
  },
  {
    id: 6,
    text: "How many close friends do you have in your circle?",
    field: "friends_circle_size",
    type: "number",
    min: 0,
    placeholder: "Number of friends"
  },
  {
    id: 7,
    text: "How many times do you post on social media in a typical week?",
    field: "post_frequency",
    type: "number",
    min: 0,
    placeholder: "Posts per week"
  }
];

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [predictionId, setPredictionId] = useState(null);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [currentValue, setCurrentValue] = useState('');

  const handleNext = () => {
    const question = personalityQuestions[currentQuestion];
    let value = currentValue;
    
    // Validate input based on question type
    if (question.type === 'number') {
      if (value === '' || isNaN(value) || value < (question.min || 0)) {
        setError(`Please enter a valid value ${question.min !== undefined ? `(minimum ${question.min})` : ''}`);
        return;
      }
      if (question.max !== undefined && value > question.max) {
        setError(`Value must be at most ${question.max}`);
        return;
      }
      value = parseInt(value);
    }
    
    // Store the answer
    const newAnswers = {...answers, [question.field]: value};
    setAnswers(newAnswers);
    setError(null);
    
    // Move to the next question or predict if all questions are answered
    if (currentQuestion < personalityQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setCurrentValue('');
    } else {
      // All questions answered, make prediction
      makePrediction(newAnswers);
    }
  };

  const handleBooleanAnswer = (value) => {
    const question = personalityQuestions[currentQuestion];
    const newAnswers = {...answers, [question.field]: value};
    setAnswers(newAnswers);
    setError(null);
    
    // Move to the next question or predict if all questions are answered
    if (currentQuestion < personalityQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setCurrentValue('');
    } else {
      // All questions answered, make prediction
      makePrediction(newAnswers);
    }
  };

  const makePrediction = async (finalAnswers) => {
    setLoading(true);
    setError(null);
    
    try {
      // Make API call with the structured data
      const response = await predictPersonality(finalAnswers);
      
      setPrediction(response);
      setPredictionId(response.prediction_id);
      setLoading(false);
    } catch (err) {
      console.error('Error making prediction:', err);
      setError('Error getting prediction. Please try again.');
      setLoading(false);
    }
  };

  const handleFeedback = async (isCorrect) => {
    if (!predictionId) return;
    
    try {
      await submitFeedback(predictionId, isCorrect ? 'correct' : 'incorrect');
      setFeedbackSubmitted(true);
    } catch (err) {
      console.error('Error submitting feedback:', err);
    }
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setAnswers({});
    setPrediction(null);
    setError(null);
    setPredictionId(null);
    setFeedbackSubmitted(false);
    setCurrentValue('');
  };

  const renderQuestionInput = () => {
    const question = personalityQuestions[currentQuestion];
    
    if (question.type === 'boolean') {
      return (
        <div className="d-grid gap-2 d-md-flex justify-content-md-center mt-4">
          <Button 
            variant="outline-success" 
            size="lg" 
            onClick={() => handleBooleanAnswer(true)}
            disabled={loading}
          >
            Yes
          </Button>
          <Button 
            variant="outline-danger" 
            size="lg" 
            onClick={() => handleBooleanAnswer(false)}
            disabled={loading}
          >
            No
          </Button>
        </div>
      );
    } else if (question.type === 'number') {
      return (
        <Form className="mt-4">
          <Form.Group>
            <Form.Control
              type="number"
              min={question.min}
              max={question.max}
              placeholder={question.placeholder}
              value={currentValue}
              onChange={(e) => setCurrentValue(e.target.value)}
              className="mb-3"
            />
            <Button 
              variant="primary" 
              onClick={handleNext}
              disabled={loading}
            >
              Next
            </Button>
          </Form.Group>
        </Form>
      );
    }
  };
  return (
    <Container className="my-5 quiz-container">
      <Row className="justify-content-center mb-4">
        <Col xs={12} md={10}>
          <Card className="shadow-sm">
            <Card.Header className="bg-primary text-white text-center">
              <h1 className="h3 mb-0">Personality Type Prediction</h1>
            </Card.Header>
            <Card.Body>
              {error && <Alert variant="danger">{error}</Alert>}
              
              {!prediction ? (
                <div>
                  <h2 className="h4 mb-4">Question {currentQuestion + 1} of {personalityQuestions.length}</h2>
                  <ProgressBar 
                    now={(currentQuestion / personalityQuestions.length) * 100} 
                    className="mb-4" 
                  />
                  
                  <Card className="mb-4 border-0 shadow-sm">
                    <Card.Body>
                      <p className="lead">{personalityQuestions[currentQuestion].text}</p>
                      
                      {/* Render the appropriate input based on question type */}
                      {personalityQuestions[currentQuestion].type === 'boolean' ? (
                        <div className="d-grid gap-2 d-md-flex justify-content-md-center mt-4">
                          <Button 
                            variant="outline-success" 
                            size="lg" 
                            onClick={() => handleBooleanAnswer(true)}
                            disabled={loading}
                          >
                            Yes
                          </Button>
                          <Button 
                            variant="outline-danger" 
                            size="lg" 
                            onClick={() => handleBooleanAnswer(false)}
                            disabled={loading}
                          >
                            No
                          </Button>
                        </div>
                      ) : (
                        <Form className="mt-4">
                          <Form.Group>
                            <Form.Control
                              type="number"
                              min={personalityQuestions[currentQuestion].min}
                              max={personalityQuestions[currentQuestion].max}
                              placeholder={personalityQuestions[currentQuestion].placeholder}
                              value={currentValue}
                              onChange={(e) => setCurrentValue(e.target.value)}
                              className="mb-3"
                            />
                            <div className="d-grid gap-2 d-md-flex justify-content-md-center">
                              <Button 
                                variant="primary" 
                                onClick={handleNext}
                                disabled={loading}
                              >
                                Next
                              </Button>
                            </div>
                          </Form.Group>
                        </Form>
                      )}
                    </Card.Body>
                  </Card>
                </div>
              ) : (
                <div className="text-center">
                  <h2 className="mb-4">Your Personality Type Prediction</h2>
                  
                  <div className="mb-4">
                    <Badge 
                      pill 
                      bg={prediction.class === 'Introvert' ? 'primary' : 'warning'} 
                      className="personality-badge"
                    >
                      {prediction.class}
                    </Badge>
                  </div>
                    <Card className="mb-4 prediction-card">
                    <Card.Body>
                      <h3 className="h5 mb-3">Probability Breakdown</h3>
                      
                      <div className="mb-3">
                        <div className="d-flex justify-content-between mb-1">
                          <span>Extrovert</span>
                          <span>{Math.round(prediction.probability[0] * 100)}%</span>
                        </div>
                        <ProgressBar 
                          variant="warning" 
                          now={prediction.probability[0] * 100} 
                          className="mb-3"
                        />
                      </div>
                      
                      <div className="mb-3">
                        <div className="d-flex justify-content-between mb-1">
                          <span>Introvert</span>
                          <span>{Math.round(prediction.probability[1] * 100)}%</span>
                        </div>
                        <ProgressBar 
                          variant="primary" 
                          now={prediction.probability[1] * 100} 
                        />
                      </div>
                    </Card.Body>
                  </Card>
                  
                  {prediction.feature_details && (
                    <Card className="mb-4 prediction-card">
                      <Card.Body>
                        <h3 className="h5 mb-3">Your Input Details</h3>
                        <table className="table table-striped">
                          <tbody>
                            <tr>
                              <td>Time Spent Alone</td>
                              <td>{prediction.feature_details.time_spent_alone} hours/day</td>
                            </tr>
                            <tr>
                              <td>Stage Fear</td>
                              <td>{prediction.feature_details.stage_fear ? "Yes" : "No"}</td>
                            </tr>
                            <tr>
                              <td>Social Event Attendance</td>
                              <td>{prediction.feature_details.social_event_attendance} events/month</td>
                            </tr>
                            <tr>
                              <td>Going Outside</td>
                              <td>{prediction.feature_details.going_outside} days/week</td>
                            </tr>
                            <tr>
                              <td>Drained After Socializing</td>
                              <td>{prediction.feature_details.drained_after_socializing ? "Yes" : "No"}</td>
                            </tr>
                            <tr>
                              <td>Friends Circle Size</td>
                              <td>{prediction.feature_details.friends_circle_size} friends</td>
                            </tr>
                            <tr>
                              <td>Post Frequency</td>
                              <td>{prediction.feature_details.post_frequency} posts/week</td>
                            </tr>
                          </tbody>
                        </table>
                      </Card.Body>
                    </Card>
                  )}
                  
                  {!feedbackSubmitted ? (
                    <div className="feedback-buttons mb-4">
                      <p>Was this prediction accurate?</p>
                      <Button 
                        variant="outline-success" 
                        onClick={() => handleFeedback(true)}
                      >
                        Yes, it's correct
                      </Button>
                      <Button 
                        variant="outline-danger" 
                        onClick={() => handleFeedback(false)}
                      >
                        No, it's incorrect
                      </Button>
                    </div>
                  ) : (
                    <Alert variant="success" className="mb-4">
                      Thank you for your feedback!
                    </Alert>
                  )}
                  
                  <Button 
                    variant="primary" 
                    size="lg" 
                    onClick={resetQuiz}
                  >
                    Take the Quiz Again
                  </Button>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
