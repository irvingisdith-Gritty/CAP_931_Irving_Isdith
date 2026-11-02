# CAP 931 - LLM Model Comparison
# Compare response time, token usage, and output quality.

import time
import csv
from groq import Groq

client = Groq()

MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]

SYSTEM_PROMPT = (
    "You are a professional B2B sales analyst. "
    "Only use the information supplied. "
    "Do not invent facts or statistics. "
    "Clearly label assumptions and unverified claims."
)

TEST_PROMPT = """
You are preparing a sales intelligence report.

Company: Microsoft
Product: Gritty Cloud Control
Target Customer: Enterprise IT departments

Verified company information:
Microsoft provides cloud computing services through Azure.

User-provided product claim:
Gritty Cloud Control helps organizations monitor cloud infrastructure.

Generate a concise report with these sections:

1. Executive Summary
2. Customer Challenges
3. Product Value Proposition
4. Competitive Landscape
5. Risks and Assumptions

Requirements:
- Do not invent statistics.
- Do not invent competitors or executive names.
- Clearly distinguish verified information from user claims.
- Identify information that requires further verification.
"""

results = []

for model in MODELS:

    print(f"\nTesting model: {model}")

    try:
        start_time = time.perf_counter()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": TEST_PROMPT},
            ],
            temperature=0,
            max_completion_tokens=3000,
        )

        elapsed = round(time.perf_counter() - start_time, 3)

        output = response.choices[0].message.content or ""

        usage = response.usage

        input_tokens = usage.prompt_tokens if usage else None
        output_tokens = usage.completion_tokens if usage else None

        results.append({
            "model": model,
            "response_time_seconds": elapsed,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "response": output,
        })

        print(f"Response time: {elapsed} seconds")
        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print("Response generated successfully.")

    except Exception as error:
        print(f"Model failed: {error}")

with open("model_comparison_results.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "model",
            "response_time_seconds",
            "input_tokens",
            "output_tokens",
            "response",
        ],
    )

    writer.writeheader()
    writer.writerows(results)

print("\nComparison complete.")
print("Results saved to model_comparison_results.csv")