# Force the library to be current
import google.generativeai as genai

# ... after genai.configure ...

# Instead of just picking a model, let's try 1.5-flash, 
# but if it fails, the error will be clearer.
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()