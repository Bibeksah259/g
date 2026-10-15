import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

st.set_page_config(page_title="My AI Chatbot", page_icon="💬")
st.title("💬 My AI Chatbot")
st.caption("Ask a question and the AI will reply.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show the conversation so far.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your message")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error("I can't find OPENAI_API_KEY. Add it to your .env file and restart the app.")
    else:
        try:
            client = OpenAI(api_key=api_key)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.responses.create(
                        model=os.getenv("OPENAI_MODEL", "gpt-6-astra"),
                        instructions="You are a helpful, friendly chatbot. Give clear answers.",
                        input=st.session_state.messages,
                    )

                    answer = response.output_text
                    st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except OpenAIError as error:
            st.error(f"The API request failed: {error}")