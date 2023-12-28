from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

with open("gpt_prompt.txt", "r") as file:
    prompt = file.read().rstrip()


def generate_summary(text):
    completion = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
      ]
    )
    return completion.choices[0].message.content
