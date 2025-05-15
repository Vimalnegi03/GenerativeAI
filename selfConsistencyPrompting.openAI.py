from dotenv import load_dotenv
import os
from openai import OpenAI
from collections import Counter
import time

# Load your API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Your question
user_question = "Who was better captian america or ironman"

# Create a base prompt for self-consistency
base_prompt = f"""
Solve the following math problem carefully:

Problem: {user_question}

- Think about it in at least 5 different ways.
- For each way, explain your reasoning step-by-step.
- Then, based on your different ways, choose the most common final answer.
- Clearly state the final result at the end.

Only output the final answer at the end in format: Final Answer: <your answer>
"""

# Number of independent thoughts (the more, the better the consistency)
num_thoughts = 5

# Store all answers
answers = []

for i in range(num_thoughts):
    response = client.chat.completions.create(
        model="gpt-4o",  # you can also use gpt-4 / gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a careful query resolver."},
            {"role": "user", "content": base_prompt}
        ],
        temperature=1.0  # High randomness to encourage different thinking paths
    )
    output_text = response.choices[0].message.content
    print(f"Response {i+1}: {output_text}")
    
    # Extract final answer
    if "Final Answer:" in output_text:
        final_answer = output_text.split("Final Answer:")[-1].strip()
        answers.append(final_answer)
    
    # Optional: small delay to avoid rate limits
    time.sleep(1)

# Find the most common final answer
counter = Counter(answers)
most_common_answer, count = counter.most_common(1)[0]

print("\nAll Answers:", answers)
print(f"\n✅ Most Consistent Final Answer: {most_common_answer} (appeared {count} times)") 