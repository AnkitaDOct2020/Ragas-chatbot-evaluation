import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

questions = pd.read_csv("questions.csv")
results = []

for _, row in questions.iterrows():
    response = model.generate_content(row["question"])

    results.append({
        "question": row["question"],
        "expected_answer": row["expected_answer"],
        "actual_answer": response.text
    })

output = pd.DataFrame(results)
output.to_csv("results/output.csv", index=False)

print(output)
print("Evaluation complete")