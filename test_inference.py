import streamlit as st
import pandas as pd
from huggingface_hub import InferenceClient

HF_TOKEN = "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"
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

client = InferenceClient(model=MODEL, token=HF_TOKEN)
prompt = "User: What is the capital of France?\nAssistant:"
response = client.text_generation(prompt, max_new_tokens=32)
print("Response:", response)

# st.title("Hello, Streamlit!")
st.header("Structured datasets")



with st.form("my_form"):

    st.subheader("dataframes")
    name=st.text_input("Enter your name")
    feedback=st.text_area("Enter your feedback")

    st.radio("Rate us",[1,2,3,4,5])
    
    st.form_submit_button("Submit")