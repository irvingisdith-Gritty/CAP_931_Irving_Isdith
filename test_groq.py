# CAP 931 - Groq API Connection Test

from groq import Groq

# Step 1: Create the Groq client
client = Groq()

# Step 2: Send a prompt to the AI model
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "You are a professional cybersecurity sales assistant."
        },
        {
            "role": "user",
            "content": "Explain cloud security in two simple sentences."
        }
    ]
)

# Step 3: Display the response
print("AI RESPONSE:")
print(response.choices[0].message.content)
