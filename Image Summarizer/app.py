import streamlit as st
import requests
import validators
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import time

# Configure Google AI
genai.configure(api_key="AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c")
image_model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Custom CSS for animations and styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: black;
}

.title-text {
    font-size: 2.5rem !important;
    color: #2c3e50 !important;
    text-align: center;
    margin-bottom: 30px !important;
    font-weight: 600;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.upload-box {
    border: 2px dashed #4a90e2;
    border-radius: 15px;
    padding: 20px;
    background: rgba(255,255,255,0.9);
    transition: all 0.3s ease;
}

.upload-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# App Layout
st.markdown('<h1 class="title-text">🎨 Image Insight Generator</h1>', unsafe_allow_html=True)

# Sidebar for Image Upload
st.sidebar.markdown("## Upload Image")
uploaded_file = st.sidebar.file_uploader("📤 Upload Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main Input Section
url = st.text_input("🌐 Enter Image URL:", placeholder="Paste image URL here...")

# Image Display
img = None
if uploaded_file or url:
    if uploaded_file:
        img = Image.open(uploaded_file)
    elif validators.url(url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
        except:
            st.error("❌ Failed to load image from URL")

    if img:
        st.image(img, use_container_width=True)
        st.success("✅ Image loaded successfully!")

# Generate Description
if st.button("✨ Generate Description", type="primary", use_container_width=True, key="generate_btn"):
    if img:
        with st.spinner("Generating description..."):
            time.sleep(1)  # Simulate processing delay
            
            try:
                response = image_model.generate_content([
                    "Describe this image in detail, including colors, composition, objects, and potential context", img
                ])
                st.markdown(f'<h3>📝 Generated Description</h3><p>{response.text}</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error generating description: {str(e)}")
    else:
        st.warning("⚠️ Please upload an image or enter a valid URL first")
