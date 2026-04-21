import streamlit as st
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
from PIL import Image
import os

# 1. Setup
st.set_page_config(page_title="Sahara Farm Brain", page_icon="🌱")
st.title("🌱 Sahara Farm Brain")

# Load API Key securely
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found. Please set it in .streamlit/secrets.toml for local testing.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Setup Vector Memory
# We create a folder called 'farm_memory' to store the vectors
client = chromadb.PersistentClient(path="./farm_memory")
embedding_func = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=api_key)
collection = client.get_or_create_collection(name="farm_logs", embedding_function=embedding_func)

# 3. Memory Functions
def retrieve_memory(query):
    try:
        results = collection.query(query_texts=[query], n_results=3)
        return "\n".join(results['documents'][0]) if results['documents'][0] else ""
    except:
        return ""

# 4. User Interface
uploaded_file = st.file_uploader("Upload farm photo...", type=["jpg", "png"])

if prompt := st.chat_input("Ask about your farm..."):
    # A. Retrieve context
    past_memory = retrieve_memory(prompt)
    full_prompt = f"Use this past history context to inform your answer: {past_memory}. User Question: {prompt}"
    
    # B. Generate
    with st.spinner("Analyzing..."):
        if uploaded_file:
            img = Image.open(uploaded_file)
            response = model.generate_content([full_prompt, img])
        else:
            response = model.generate_content(full_prompt)
        
    st.write(response.text)
    
    # C. Save interaction
    entry = f"Date: {datetime.now().strftime('%Y-%m-%d')} | Query: {prompt} | Response: {response.text}"
    collection.add(documents=[entry], ids=[str(datetime.now().timestamp())])