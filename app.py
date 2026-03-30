from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Hola, dime algo inteligente"}
    ]
)

print(response.choices[0].message.content)
