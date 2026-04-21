import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Sahara Farm Brain", page_icon="🌱")
st.title("🌱 Sahara Farm Brain")

# 2. API CONFIGURATION (This must be here)
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# THIS IS THE PART THAT CONNECTS YOU TO GOOGLE
genai.configure(api_key=api_key)

# 3. DEBUGGER: This will tell us if your model name is wrong
if st.button("Check Available Models"):
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write("Models you can use:", models)
    except Exception as e:
        st.error(f"Error listing models: {e}")

# 4. Initialize Model
# Change this string to one of the names you see in the "Check Available Models" list
# e.g., 'gemini-1.5-flash' or 'gemini-2.0-flash'
model_name = 'gemini-1.5-flash' 
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Could not load model '{model_name}': {e}")
    st.stop()

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input
uploaded_file = st.file_uploader("Upload a farm photo...", type=["jpg", "jpeg", "png"])
user_prompt = st.chat_input("Ask about your plants...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner("Analyzing..."):
        try:
            content = [user_prompt]
            if uploaded_file:
                content.append(Image.open(uploaded_file))
            
            response = model.generate_content(content)
            
            st.chat_message("assistant").markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")