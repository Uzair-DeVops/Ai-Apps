import streamlit as st
import tempfile
import time
from pathlib import Path
import os
import google.generativeai as genai
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service.json"

genai.configure(api_key="AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c")



def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )





multimodal_Agent = initialize_agent()

st.title("Video Summarizer")
st.write("upload your video")
video_file = st.sidebar.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name
    st.video(video_path, format="video/mp4")

if video_file:
    with st.form(key='video_form'):
                # Text area for user query about the video
                user_query_video = st.text_area("What insights are you seeking from the video?")

                # Button to analyze the video
                submit_button = st.form_submit_button("🔍 Analyze Video")

                if submit_button:
                    if not user_query_video:
                        st.warning("Please enter a question or insight to analyze the video.")
                    else:
                        try:
                            with st.spinner("Processing video and gathering insights..."):
                                # Process the video for analysis
                                processed_video = upload_file(video_path)
                                while processed_video.state.name == "PROCESSING":
                                    time.sleep(1)
                                    processed_video = get_file(processed_video.name)

                                # Prompt generation for video analysis
                                analysis_prompt = f"Analyze the uploaded video for content and context. Respond to the following query using video insights: {user_query_video}"

                                # Run the multimodal agent for analysis
                                response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])

                            # Display the result
                            st.subheader("Analysis Result")
                            st.markdown(response.content)

                        except Exception as error:
                            st.error(f"An error occurred during analysis: {error}")
                        finally:
                            Path(video_path).unlink(missing_ok=True)

