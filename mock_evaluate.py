# mock_evaluate.py
import pandas as pd

# Read questions from CSV
# questions.csv should contain:
# question,expected_answer

df = pd.read_csv("questions.csv")

results = []
passed = 0
total = len(df)


def get_answer(question):
    sample_answers = {
        "What is the capital of India?": "New Delhi",
        "Who wrote Hamlet?": "William Shakespeare",
        "What is the largest planet in our solar system?": "Jupiter",
        "What is the boiling point of water in Celsius?": "100 degrees Celsius",
        "Who painted the Mona Lisa?": "Leonardo da Vinci",
        "What is the currency of Japan?": "Yen",
        "What is the chemical symbol for gold?": "Au",
        "Who is known as the father of computers?": "Charles Babbage",
        "What is the fastest land animal?": "Cheetah",
        "In which year did India gain independence?": "1947"
    }

    return sample_answers.get(question, "No answer")



def evaluate_answer(expected, answer):
    expected_words = expected.lower().split()
    answer_lower = answer.lower()

    return all(word in answer_lower for word in expected_words)


for _, row in df.iterrows():
    question = row["question"]
    expected = row["expected_answer"]

    answer = get_answer(question)

    if evaluate_answer(expected, answer):
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(" " + "=" * 60)
    print("Question :", question)
    print("Expected :", expected)
    print("Actual   :", answer)
    print("Result   :", status)

    results.append({
        "question": question,
        "expected": expected,
        "actual": answer,
        "result": status
    })


report_df = pd.DataFrame(results)
report_df.to_csv("results.csv", index=False)

accuracy = (passed / total) * 100

print(" " + "=" * 60)
print("Final Score:", passed, "/", total)
print("Accuracy   :", round(accuracy, 2), "%")
print("Report saved to results.csv")