import torch
import streamlit as st
# Use a pipeline as a high-level helper
from transformers import pipeline
import re
# Specify that you want to load the model as a PyTorch model
pipe = pipeline("text-generation", model="ammarahad17/Pakwiki_model", framework="pt")


st.markdown("<h2 style='text-align: center; color:green;'>Pakistan</h2>", unsafe_allow_html=True)

# Initialize the messages attribute if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        generated_text = ''
        pipe(prompt, do_sample=False)
        generated_text = pipe(prompt, num_return_sequences=10, return_full_text=True)
        extracted_text = [response["generated_text"] for response in generated_text]
        # Clean the generated text
        cleaned_text = []
    for text in extracted_text:
    # Use regex to match the question part and remove it
        cleaned_text_part = re.sub(r'^.*\? \n\n—["[1-9]', '', text)
        cleaned_text.append(cleaned_text_part)
        message_placeholder.markdown(cleaned_text)
        st.session_state.messages.append({"role": "assistant", "content": cleaned_text})













