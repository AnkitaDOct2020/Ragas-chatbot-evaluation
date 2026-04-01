import pandas as pd
from openai import OpenAI
import time
from difflib import SequenceMatcher

# Load questions
df = pd.read_csv("questions.csv")

# List of models to test
models = [
    "google/gemma-3-4b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free"
]

# Initialize OpenAI client (replace with your key)
client = OpenAI(api_key="YOUR_API_KEY", base_url="https://openrouter.ai/api/v1")

#Get answer from model
def get_answer(question, model_name):
    retries = 3

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message.content

        except Exception as e:
            error_message = str(e)

            if attempt < retries - 1:
                print(f"Retrying... attempt {attempt + 1}")
                time.sleep(5)
            else:
                return f"ERROR: {error_message}"

#Evaluate answer
def evaluate_answer(expected, answer):
    expected = expected.lower().strip()
    answer = answer.lower().strip()

    if expected in answer:
        return True

    similarity = SequenceMatcher(None, expected, answer).ratio()

    return similarity >= 0.6

summary = []
# Loop through models
for model_name in models:
    print("\n" + "#" * 60)
    print(f"Testing Model: {model_name}")
    print("#" * 60)

    passed = 0
    total = len(df)
    results = []
    errors = []
    total_time = 0
    failed_questions = []
    error_count = 0
    for _, row in df.iterrows():
        question = row["question"]
        expected = row["expected_answer"]

        start_time = time.time()
        answer = get_answer(question, model_name)
        end_time = time.time()

        response_time = round(end_time - start_time, 2)
        total_time += response_time

        if evaluate_answer(expected, answer):
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            if "ERROR" in answer:
                errors.append({"model": model_name, "question": question, "error": answer})
                error_count += 1
            failed_questions.append({
                "model": model_name,
                "question": question,
                "expected": expected,
                 "actual": answer
                })

        print("\n" + "=" * 60)
        print("Question :", question)
        print("Expected :", expected)
        print("Actual   :", answer)
        print("Result   :", status)
        print("Time     :", response_time, "seconds")
        #Save reports
        results.append({
            "model": model_name,
            "question": question,
            "expected": expected,
            "actual": answer,
            "result": status,
            "response_time_seconds": response_time
        })
        #Load CSV
        if failed_questions:
         failed_df = pd.DataFrame(failed_questions)
         failed_df.to_csv(
            f"failed_{model_name.replace('/', '_')}.csv",
            index=False
            )

    # Save results and errors
    pd.DataFrame(results).to_csv(f"results_{model_name.replace('/', '_')}.csv", index=False)
    if errors:
        pd.DataFrame(errors).to_csv(f"errors_{model_name.replace('/', '_')}.csv", index=False)

    accuracy = (passed / total) * 100
    average_time = round(total_time / total, 2)

    summary.append({
    "model": model_name,
    "accuracy": round(accuracy, 2),
    "average_time_seconds": average_time,
    "errors": error_count

    })
    print("\n" + "=" * 60)
    print(f"Model: {model_name}")
    print("Final Score:", passed, "/", total)
    print("Accuracy   :", round(accuracy, 2), "%")
    print("Average Time:", average_time, "seconds")
    print(f"Results saved to results_{model_name.replace('/', '_')}.csv")
    if errors:
        print(f"Errors saved to errors_{model_name.replace('/', '_')}.csv")

    #Load CSV
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv("summary.csv", index=False)

    print("Summary saved to summary.csv")