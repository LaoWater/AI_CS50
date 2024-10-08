from openai import OpenAI

client = OpenAI()

# Using GPT 4-O
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[

        {"role": "system",
         "content": "You are a helpful math tutor. Guide the user through the solution step by step. "
                    "Format the response in beautiful paragraphs."
                    "Before starting to solve, provide the user the needed formulas to solve it himself."},

        {"role": "user",
         "content": "how can I solve 8^x + sqrt(7x+1) = 23"}
    ]
)

response = completion.choices[0].message

# Print the response in a formatted way
print(response.content)
