from pathlib import Path
import streamlit as st
from groq import Groq
import yaml
import os
import re


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
            {"role": "user", "content": input_prompt},
        ],
        # model="llama3-8b-8192",
        model="llama-3.3-70b-versatile",
        # model="mixtral-8x7b-32768",
        # model="llama-guard-3-8b",
    )

    return chat_completion.choices[0].message.content.strip()


def main():
    # Configure Groq API
    regex_reasoning = r"<reasoning>(.*?)</reasoning>"
    regex_output = r"<output>(.*?)</output>"
    client = Groq(api_key=st.secrets.GROQ_API_KEY)

    st.write("Modération de contenu application Entourage.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Let's start chatting! 👇"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        response = moderate_text(client, prompt)
        message_placeholder = st.empty()

        reasoning_match = re.search(regex_reasoning, response, re.DOTALL)
        output_match = re.search(regex_output, response, re.DOTALL)
        reasoning_text = reasoning_match.group(1).strip() if reasoning_match else None
        output_text = output_match.group(1).strip() if output_match else None

        if reasoning_text is None or output_text is None:
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            message_placeholder.markdown(
                f"""Raisonnement : {reasoning_text}
                
                Message {output_text}"""
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": reasoning_text}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": output_text}
            )


if __name__ == "__main__":
    main()
