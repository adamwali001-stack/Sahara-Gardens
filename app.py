import streamlit as st
import google.generativeai as genai

st.title("🌱 Sahara Farm Brain - Heartbeat Test")

# 1. Get the key from Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found in Streamlit Secrets!")
    st.stop()

# 2. Setup the connection
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # 3. Test the connection
    if st.button("Check Connection"):
        response = model.generate_content("Say 'System Operational'")
        st.success(f"Connection Successful! AI says: {response.text}")
        
except Exception as e:
    st.error(f"Connection Error: {e}")