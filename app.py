import streamlit as st
import google.generativeai as genai

# 1. Page Configuration (Makes it look nice on Mobile)
st.set_page_config(page_title="AI Language Tutor", page_icon="🗣️", layout="centered")

# 2. Configure Gemini API safely using Streamlit Secrets
# (If testing locally, replace st.secrets[...] with your actual string "AIzaSy...")
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please set your GEMINI_API_KEY in your Streamlit Secrets or environment variables.")
    st.stop()

# 3. Define the AI Teacher Persona
SYSTEM_INSTRUCTION = """
You are 'Maestro', a friendly, patient, and highly encouraging personal AI Language Teacher.
Your goal is to help the user practice their target language through natural conversation.

Follow these strict rules:
1. Identify the language the user wants to learn (ask them if you aren't sure).
2. Keep your responses relatively short (2-4 sentences) so the user doesn't get overwhelmed.
3. If the user makes a grammar or spelling mistake, gently correct them using a '🔧 Correction:' block before continuing the conversation.
4. Provide translations in brackets [like this] for any advanced or difficult words you use.
5. Always end your response with an engaging question to keep the chat flowing.
"""

# 4. Initialize the AI Model & Chat Session
if "chat_session" not in st.session_state:
    # Initialize the Gemini 1.5 Flash model (great for fast, conversational text)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=SYSTEM_INSTRUCTION
    )
    # Start an ongoing chat session
    st.session_state.chat_session = model.start_chat(history=[])

# 5. UI Layout
st.title("🗣️ Your Personal AI Language Teacher")
st.caption("Practice speaking any language! Your teacher will chat with you and gently correct your mistakes.")
st.divider()

# 6. Display Chat History (keeps older messages visible on screen)
# Gemini's history stores roles as 'user' and 'model'
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 7. Handle New User Input
if user_input := st.chat_input("Type your message here... (e.g., 'Bonjour!', 'Hola, cómo estás?')"):
    
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Send message to Gemini and get the stream response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Teacher is thinking..."):
            response = st.session_state.chat_session.send_message(user_input)
            response_placeholder.markdown(response.text)
