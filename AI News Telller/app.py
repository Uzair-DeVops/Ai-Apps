import streamlit as st
import requests
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from datetime import datetime

# Custom CSS for styling
# Custom CSS for dark theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    color: #ffffff;
}

.header-container {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    border-radius: 0 0 20px 20px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.search-box {
    max-width: 600px;
    margin: 0 auto;
    position: relative;
}

.news-card {
    background: #2d2d2d;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-left: 4px solid #4a90e2;
}

.news-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(74,144,226,0.2);
    background: #363636;
}

.news-image {
    border-radius: 10px;
    margin-bottom: 1rem;
    max-height: 200px;
    object-fit: cover;
    border: 2px solid #3a3a3a;
}

.loading-animation {
    display: flex;
    justify-content: center;
    padding: 2rem 0;
}

.dot-pulse {
    position: relative;
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background-color: #00f2fe;
    color: #00f2fe;
    animation: dotPulse 1.5s infinite linear;
}

@keyframes dotPulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.5; }
    100% { transform: scale(1); opacity: 1; }
}

.source-badge {
    background: #2ecc71;
    color: #000000;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.stTextInput>div>div>input {
    color: #ffffff !important;
    background-color: #2d2d2d !important;
    border: 1px solid #4a90e2 !important;
    border-radius: 10px !important;
}

.stButton>button {
    background: linear-gradient(135deg, #00f2fe 0%, #4a90e2 100%) !important;
    color: #000000 !important;
    border: none !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    margin-top: 25px;
}

.stButton>button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 15px rgba(0,242,254,0.4) !important;
}

a {
    color: #00f2fe !important;
    text-decoration: none !important;
}

a:hover {
    text-decoration: underline !important;
}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="header-container">
    <h1>📰 News Explorer</h1>
    <p>Discover the latest news from around the world</p>
</div>
""", unsafe_allow_html=True)

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c")

@tool
def get_latest_news(topic: str) -> str:
    """Fetches latest news articles for a given topic"""
    api_key = "e9c6d47717ab4738b733f4a8e15f9375"
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&sortBy=publishedAt"

    try:
        with st.spinner(""):
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data.get('articles'):
                return data['articles']
            return []
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

# Search Interface
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("", placeholder="Enter news topic (e.g., Technology, Politics...)")

with col2:
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.search_triggered = True

# Display Results
if 'search_triggered' in st.session_state and query:
    articles = get_latest_news(query)
    
    if articles:
        st.subheader(f"Latest News on {query.title()}", divider="blue")
        
        for article in articles[:10]:
            with st.container():
                col_img, col_text = st.columns([1, 2])
                
                with col_img:
                    if article['urlToImage']:
                        st.image(article['urlToImage'], use_container_width=True, 
                               caption=article['source']['name'], 
                               output_format="PNG")
                
                with col_text:
                    st.markdown(f"""
                    <div class="news-card">
                        <div class="source-badge">
                            {article['source']['name']} • {datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y")}
                        </div>
                        <h3>{article['title']}</h3>
                        <p>{article['description'] or 'No description available'}</p>
                        <a href="{article['url']}" target="_blank" style="text-decoration: none; color: #3498db;">
                            Read more →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
    elif isinstance(articles, list):
        st.warning("No articles found for this topic")
    else:
        st.error("Failed to fetch news articles")