import streamlit as st
from langchain_groq import ChatGroq
import requests
import http.client
import json
import time

# Custom CSS with animations and styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: black;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 1s ease-in;
}

.article-card {
    background: darkslategray;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 2rem 0;
    backdrop-filter: blur(8px);
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}

.glow-text {
    text-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("About")
    st.markdown("---")
    st.markdown("### Created by: Muhammad Uzair")
    st.markdown("**AI-Powered Article Generator**")
    st.markdown("Version 1.0 | Powered by Groq & Serper API")

# Main app title
st.title("📝 AI Article Writer")
st.markdown('<div class="glow-text">Crafting well-researched articles with AI-powered insights</div>', unsafe_allow_html=True)

# Initialize Groq model
def initialize_model():
    try:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key="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"
        )
    except Exception as e:
        st.error(f"Model initialization failed: {str(e)}")
        return None

# Serper API search function
def search_web(query: str):
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': '6f2bfdd501e9a4a2f99d8d81455b199912490100',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        response = conn.getresponse()
        return json.loads(response.read().decode())
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return None

# Unsplash image search
def search_images(query: str):
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": query,
                "client_id": "YcKCA72Ez-w6bn0jC03opmr4UtdeXlRccoHpOs4WygU",
                "per_page": 3
            },
            timeout=10
        )
        response.raise_for_status()
        return [img['urls']['regular'] for img in response.json()['results']]
    except Exception as e:
        st.error(f"Image search failed: {str(e)}")
        return []

# Article generation prompt
def create_prompt(topic: str, search_data: dict):
    return f"""
Generate a comprehensive article about: {topic}
Incorporate information from these search results: {json.dumps(search_data)[:3000]}

Structure:
1. Introduction (Overview and significance)
2. Historical Context (Origin and evolution)
3. Current Trends (Latest developments and applications)
4. Key Facts (Important statistics and research findings)
5. Challenges (Current limitations and debates)
6. Future Outlook (Predictions and potential developments)
7. Conclusion (Summary and final thoughts)

Formatting Requirements:
- Use Markdown with proper headings
- Include bullet points for key items
- Add relevant examples/case studies
- Maintain professional yet engaging tone
- Optimize for SEO with relevant keywords
- Minimum 1500 words
"""

# Main execution flow
def main():
    user_input = st.text_input("Enter your article topic:", 
                             placeholder="e.g., Artificial Intelligence in Modern Healthcare")
    
    if user_input:
        model = initialize_model()
        if not model:
            return
            
        with st.status("🚀 Researching and generating your article...", expanded=True) as status:
            # Show loading animation
            st.markdown('<div class="loading-spinner">🔍 Analyzing topic...</div>', unsafe_allow_html=True)
            
            # Perform searches
            search_results = search_web(user_input)
            image_urls = search_images(user_input)
            
            if not search_results:
                st.error("Failed to gather research data")
                return
                
            # Generate article
            prompt = create_prompt(user_input, search_results)
            try:
                response = model.invoke(prompt)
                article_content = response.content
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
                return
            
            status.update(label="✅ Article ready!", state="complete", expanded=False)
        
        # Display results
        st.markdown(f'<div class="fade-in article-card">{article_content}</div>', unsafe_allow_html=True)
        
        # Provide download option for the article
        st.download_button(
            label="Download Article as Text",
            data=article_content,
            file_name=f"article_{user_input}.txt",
            mime="text/plain"
        )
        
        # Display images
        if image_urls:
            st.markdown("### 📸 Related Images")
            cols = st.columns(3)
            for idx, img_url in enumerate(image_urls):
                cols[idx % 3].image(img_url,use_container_width=True, caption=f"Image {idx+1} | Source: Unsplash")
                
                # Provide download option for images
                image_response = requests.get(img_url)
                st.download_button(
                    label=f"Download Image {idx+1}",
                    data=image_response.content,
                    file_name=f"image_{idx+1}.jpg",
                    mime="image/jpeg"
                )
        
        # Success effects
        st.balloons()
        st.success("✨ Article generated successfully!")
        
        # Footer
        st.markdown("---")
        st.markdown("<div style='text-align: center; color: #666; margin-top: 2rem;'>"
                    "🚀 Powered by Groq & Serper API | ✍️ Created by Muhammad Uzair</div>", 
                    unsafe_allow_html=True)

if __name__ == "__main__":
    main()
