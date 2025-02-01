import streamlit as st
import requests
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

# Streamlit App Title
st.title("🖼️ Image Search with AI")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c")

# Define the image search tool
@tool(parse_docstring=True)
def search_image(query: str):
    """Searches for images based on the query keyword.
    
    Args:
        query (str): The search query to find images.
    
    Returns:
        str: Displays images related to the search query.
    """
    api_key = "YcKCA72Ez-w6bn0jC03opmr4UtdeXlRccoHpOs4WygU"
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('results'):
        image_urls = [image['urls']['small'] for image in data['results'][:5]]
        return image_urls
    else:
        return []

# Streamlit UI for input
query = st.text_input("Enter a keyword to search for images:")

if st.button("🔍 Search Images"):
    if query:
        st.write(f"Searching images for: **{query}**")
        image_urls = search_image(query)
        
        if image_urls:
            for idx, img_url in enumerate(image_urls):
                # Display the image
                st.image(img_url, caption=f"Image related to {query}", use_container_width=True)
                
                # Add a download button with a unique key for each image
                st.download_button(
                    label="Download Image",
                    data=requests.get(img_url).content,
                    file_name=f"{query}_image_{idx+1}.jpg",
                    mime="image/jpeg",
                    key=f"download_button_{idx}"  # Unique key for each button
                )
        else:
            st.warning("No images found. Try a different keyword.")
    else:
        st.warning("Please enter a search keyword.")
