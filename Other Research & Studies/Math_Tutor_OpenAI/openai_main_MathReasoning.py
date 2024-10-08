from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()


class Step(BaseModel):
    explanation: str
    output: str


class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str


# Using GPT 4-O
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system",
         "content": "You are a helpful math tutor. Guide the user through the solution step by step. "
                    "Format the response in beautiful paragraphs."
                    "Before starting to solve, provide the user the needed formulas to solve it himself."},
        {"role": "user", "content": "how can I solve 8^x + sqrt(7x+1) = 23"}
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message.parsed

# Print the response in a formatted way
print("Steps to Solve the Equation:\n")
for step in math_reasoning.steps:
    print(f"{step.explanation}\nOutput: {step.output}\n")

print(f"Final Answer:\n{math_reasoning.final_answer}")