# AI Model Evaluation Framework

This project evaluates multiple AI models using a CSV file of questions and expected answers.

It supports:
- Multiple model testing
- PASS / FAIL evaluation
- Accuracy calculation
- Response time tracking
- Retry logic for API failures
- CSV reports for results, failures, errors, and summary

## Models Tested
- google/gemma-3-4b-it:free
- meta-llama/llama-3.3-70b-instruct:free

## Files
- questions.csv → Input questions and expected answers
- results_*.csv → Model-wise detailed results
- failed_*.csv → Failed questions only
- errors_*.csv → API errors only
- summary.csv → Accuracy and timing summary

## questions.csv Format

question,expected_answer
What is the capital of India?,New Delhi
Who wrote Hamlet?,William Shakespeare

## Setup

1. Install dependencies:

bash
pip install -r requirements.txt

2.Export your OpenRouter API key:
export OPENROUTER_API_KEY="your_api_key"

3.Run the project:
python evaluate.py
