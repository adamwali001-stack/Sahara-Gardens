import streamlit as st
import google.generativeai as genai

st.title("🌱 Sahara Farm Brain - Model Debugger")

api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found.")
    st.stop()

genai.configure(api_key=api_key)

if st.button("List Available Models"):
    try:
        # This will list all models your key is allowed to access
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write("Models you can use:")
        st.write(models)
    except Exception as e:
        st.error(f"Error: {e}")

user_input = st.text_input("Test a specific model name (e.g., gemini-1.5-flash):")
if st.button("Connect and Generate"):
    try:
        model = genai.GenerativeModel(user_input)
        response = model.generate_content("Say 'System Operational'")
        st.success(f"Success! AI says: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")