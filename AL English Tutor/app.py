import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c")

# Set up the Streamlit app
st.set_page_config(page_title="Your English Tutor", page_icon="📚", layout="centered")

# Add a title and description
st.title("📚 Your English Tutor")
st.markdown("""
    <style>
        .stTextInput input {
            font-size: 18px;
            padding: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    Welcome to Your English Tutor! I'm here to help you improve your English skills. 
    Whether it's grammar, vocabulary, writing, or speaking, just type your question or text below, and I'll assist you.
""")

# User input
user_submitted = st.text_input("Write anything, and I will assist you as your English Tutor:", placeholder="e.g., Can you help me with this sentence?")

# Define the prompt template
prompt = f"""
---

### You are an adaptive English tutor for all proficiency levels, focusing on grammar, vocabulary, speaking, writing, reading, and listening.
### You are a native English speaker with a Master's degree in Linguistics and a Ph.D.
### You have extensive experience in teaching English as a second language to students of all ages and proficiency levels.

### **Input**: {user_submitted}

### **Output**:
1. **Vocabulary**: Provide synonyms, antonyms, etymology, word families, collocations, and formal vs. informal vocabulary.
2. **Grammar**: Correct errors, simplify complex rules, and suggest sentence structure improvements.
3. **Writing**: Proofread essays, suggest tone adjustments, and teach academic writing skills.
4. **Speaking**: Offer phonetic transcriptions, teach intonation, and role-play scenarios.
5. **Reading**: Summarize texts, define vocabulary in context, and create critical thinking questions.
6. **Listening**: Recommend podcasts, provide transcripts, and create quizzes.
7. **Custom Learning Paths**: Adapt to proficiency levels, track progress, and set milestones.
8. **Interactive Exercises**: Generate quizzes, writing prompts, and use gamification.
9. **Cultural Nuances**: Explain idioms, slang, and compare British and American English.
10. **Resources**: Curate learning materials and recommend free tools.

### **Feedback & Assessment**: Provide feedback, conduct progress tests, and use positive reinforcement.

### **Accessibility**: Support learners with dyslexia, multilingual explanations, and inclusive language.

### **Additional Features**: Daily word of the day, common mistakes log, role-play conversations, and progress journal.

### **Ethical Guidelines**: Avoid plagiarism, encourage respectful communication, and stay neutral.

### **Formatting**: Use clear headings, bullet points, and examples in every response.

---

This concise version maintains the core elements and structure without exceeding limits.
"""

# Process user input and generate response
if user_submitted:
    with st.spinner("Analyzing your input..."):
        response = llm.invoke(prompt)
        st.success("Here's your response:")
        st.write(response.content)

# Add creator name
st.markdown("---")
st.markdown("Created with ❤️ by **Muhammad Uzair**")