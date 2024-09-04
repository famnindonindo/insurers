import os
import google.generativeai as genai
import pandas as pd
import streamlit as st
from prompt import PROMPT_INSURVERSE
from google.generativeai.types import HarmCategory, HarmBlockThreshold


genai.configure(api_key="AIzaSyDiji5U1OleJzLMM4mqYPh5w6vPga0VjmA")
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    }

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=SAFETY_SETTINGS,
    generation_config=generation_config,
    system_instruction=PROMPT_INSURVERSE
    ,)


def clear_history():
    
    st.session_state["messages"] = [
        {"role": "model", "content": "อินชัวร์เวิร์ส สวัสดีค่ะ คุณลูกค้า สอบถามข้อมูลประกันเรื่องใดคะ"}
    ]
    st.experimental_rerun()


with st.sidebar:
    if st.button("Clear History"):
        clear_history()

st.title("💬 Insurverse  สวัสดีค่ะ")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "model",
            "content": "อินชัวร์เวิร์ส สวัสดีค่ะ คุณลูกค้า สอบถามข้อมูลประกันเรื่องใดคะ",
        }
    ]

file_path = "insurverse_p1 (3).xlsx"
try:
    df = pd.read_excel(file_path)
    file_content = df.to_string(index=False)
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    def generate_response():
        history = [
            {"role": msg["role"], "parts": [{"text": msg["content"]}]}
            for msg in st.session_state["messages"]
        ]

        history.insert(1, {"role": "user", "parts": [{"text": file_content}]})

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(prompt)
        st.session_state["messages"].append({"role": "model", "content": response.text})
        st.chat_message("model").write(response.text)

    generate_response()

#print("total_tokens: ", model.count_tokens(PROMPT_INSURVERSE))
#response = model.generate_content(file_content)
#print(response.usage_metadata)
