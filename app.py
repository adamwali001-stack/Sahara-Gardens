import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Sahara Farm Brain", page_icon="🌱")
st.title("🌱 Sahara Farm Brain")

# 2. Setup Google Gemini
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Using the validated model name
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
uploaded_file = st.file_uploader("Upload a farm photo...", type=["jpg", "jpeg", "png"])
user_prompt = st.chat_input("Ask about your plants or management...")

def process_interaction(prompt, image=None):
    content = [prompt]
    if image:
        img = Image.open(image)
        content.append(img)
    
    response = model.generate_content(content)
    return response.text

# 6. Execute Chat
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner("Analyzing farm data..."):
        try:
            response_text = process_interaction(user_prompt, uploaded_file)
            st.chat_message("assistant").markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Error: {e}")