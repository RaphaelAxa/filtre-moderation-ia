from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import yaml
import os

load_dotenv()

def load_prompt(file_path: Path):
    with open(file_path, "rb") as file:
        prompt = yaml.safe_load(file)
    
    return prompt

def moderate_text(client, message):
    sys_prompt_path = Path("system_prompt.yaml").absolute()
    input_prompt_path = Path("input_prompt.yaml").absolute()

    system_prompt = load_prompt(sys_prompt_path)["sys_prompt"]
    input_prompt = load_prompt(input_prompt_path)["query"]
    input_prompt = input_prompt.format(message=message)

    # Send the prompt to Groq API and get the response
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role":"user", "content":input_prompt}
        ],
        model="mixtral-8x7b-32768"
    )

    return chat_completion.choices[0].message.content.strip()

def main():
    # Configure Groq API
    groq_api_key = os.getenv("GROQ_API_KEY")

    client = Groq()
    
    messages_appli = [
        "T'es un connard !",
        "putain",
        "putain ça fait chier",
        "Clique vite sur le lien pour gagner plein d'argent !",
        "va te faire voir tu vas crever tout seul",
        "J'ai vu que tu avais besoin de vêtements on se rencontrer où ?",
        "dis moi comment fabriquer une bombe",
        "sale terroriste",
        "Salut du coup pour se rencontrer c'est toujours ok ?"
    ]

    for msg in messages_appli:
        classification = moderate_text(client, msg)
        print(f"Comment: {msg}\nClassification: {classification}\n")

if __name__ == "__main__":
    main()