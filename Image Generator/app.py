import streamlit as st
import requests
from PIL import Image
import io

# Function to generate image
def generate_image(prompt):
    API_KEY = "8773408815b3df1c64b47ad4c943faa116cc639a9c9ec72b68c89d9be66e3d4330f1589c6735ea04a3319824216bb98e"
    
    with st.spinner('🎨 Generating your image... This might take a moment'):
        r = requests.post(
            'https://clipdrop-api.co/text-to-image/v1',
            files={'prompt': (None, prompt), 'text/plain': None},
            headers={'x-api-key': API_KEY}
        )
    
    if r.ok:
        return r.content
    else:
        st.error(f"Error: {r.status_code} - {r.text}")
        return None

# Main UI
st.set_page_config(page_title="AI Image Generator", page_icon="🖼️")

# Sidebar with info
with st.sidebar:
    st.title("About")
    st.markdown("""
    **Transform text prompts into stunning images** using AI-powered generation.
    
    ### Features:
    - Generate high-quality images from text
    - Download your creations
    - Quick processing
    """)
    
    st.markdown("---")
    st.markdown("**Example prompts:**")
    st.markdown("- A futuristic cityscape at sunset")
    st.markdown("- A surreal forest with glowing trees")
    st.markdown("- A cyberpunk cat wearing neon sunglasses")
    st.markdown("---")
    st.caption("Powered by Clipdrop API | Made with Streamlit")

# Main content
st.title("🖼️ Text-to-Image Generator")
st.markdown("Turn your imagination into visual reality! Describe your vision below and let AI create it for you.")

# Text input
prompt = st.text_area(
    label="**Your creative prompt:**",
    placeholder="Describe the image you want to generate...",
    height=150,
    help="Be as descriptive as possible for best results!"
)

# Generation section
col1, col2, col3 = st.columns([1,2,1])
with col2:
    generate_btn = st.button("✨ Generate Image", use_container_width=True)

if generate_btn and prompt:
    image_bytes = generate_image(prompt)
    
    if image_bytes:
        st.success("✅ Image generated successfully!")
        st.image(image_bytes,  use_container_width=True)
        
        # Add download button
        img = Image.open(io.BytesIO(image_bytes))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="⬇️ Download Image",
            data=byte_im,
            file_name="generated_image.png",
            mime="image/png",
            use_container_width=True
        )
    elif not image_bytes:
        st.error("Failed to generate image. Please try again.")

elif generate_btn and not prompt:
    st.warning("Please enter a prompt before generating!")

# Footer
st.markdown("---")
st.markdown("### Usage Tips:")
st.markdown("- Use descriptive adjectives (e.g., 'vibrant', 'glowing', 'futuristic')")
st.markdown("- Specify art styles if desired (e.g., 'digital art', 'watercolor painting')")
st.markdown("- Include environmental details (e.g., 'sunset lighting', 'foggy atmosphere')")

# Add some security information
st.markdown("---")
st.caption("Note: This AI system may filter certain types of content based on safety guidelines. Generated images are automatically reviewed for appropriate content.")