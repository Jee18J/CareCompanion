# import streamlit as st
# import google.generativeai as genai
# import speech_recognition as sr

# # Configure Gemini AI (use your actual API key)
# genai.configure(api_key="AIzaSyClwCo8aIpV8gieeDQ5HsjiASODhGkxt-0")

# # Model configuration (identical to your Flask version)
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config,
#     system_instruction="pediatrician work\nFor example if i ask \"My child has cough for 3 days \" means it should reply like it cold disease \nand give some common medicin names and it should give generic answers not in depth\n\n",
# )

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hello! I'm your pediatric health assistant. How can I help?"}
#     ]

# # Page layout
# st.set_page_config(page_title="Pediatric Health Assistant", page_icon="👶")
# st.title("👶 Pediatric Health Assistant")

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Function to process voice input
# def voice_input():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Please speak your question...")
#         audio = recognizer.listen(source)
        
#         # Recognizing the speech
#         try:
#             prompt = recognizer.recognize_google(audio)
#             st.success(f"You said: {prompt}")
#             return prompt
#         except sr.UnknownValueError:
#             st.error("Sorry, I could not understand the audio.")
#             return None
#         except sr.RequestError as e:
#             st.error(f"Could not request results from Google Speech Recognition service; {e}")
#             return None

# # Options for input: Text or Voice
# input_mode = st.radio("Choose your input method:", ("Text", "Voice"))

# if input_mode == "Text":
#     if prompt := st.chat_input("Ask about your child's symptoms..."):
#         # Process the prompt as normal
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 try:
#                     response = model.generate_content(prompt)
#                     st.markdown(response.text)
#                     st.session_state.messages.append({"role": "assistant", "content": response.text})
#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")

# elif input_mode == "Voice":
#     if st.button("Click to Speak"):
#         prompt = voice_input()
#         if prompt:
#             # Process the prompt as received from voice input
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     try:
#                         response = model.generate_content(prompt)
#                         st.markdown(response.text)
#                         st.session_state.messages.append({"role": "assistant", "content": response.text})
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")

# # Navigation button using native Streamlit
# st.markdown("---")
# if st.button("Detailed Symptom Checker", type="primary", use_container_width=True):
#     st.switch_page("pages/trial.py")  # Correct path to the target page/


import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from datetime import datetime
import time

# Custom CSS for modern UI
def local_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4a6fa5;
            --secondary: #166088;
            --accent: #4fc1e9;
            --background: #f8f9fa;
            --card: #ffffff;
            --text: #2c3e50;
            --warning: #ff6b6b;
            --success: #48dbb4;
        }
        
        .main {
            background-color: var(--background);
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            background-color: var(--secondary);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* Chat message styling */
        .stChatMessage {
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .stChatMessage.user {
            background-color: rgba(74, 111, 165, 0.1);
            border-left: 4px solid var(--primary);
        }
        
        .stChatMessage.assistant {
            background-color: rgba(255, 255, 255, 0.9);
            border-left: 4px solid var(--accent);
        }
        
        /* Radio buttons */
        .stRadio [role="radiogroup"] {
            gap: 15px;
            margin-bottom: 1rem;
        }
        
        .stRadio [role="radio"] {
            padding: 8px 16px;
            border-radius: 8px;
            border: 1px solid #dfe3e8;
        }
        
        .stRadio [role="radio"][aria-checked="true"] {
            background-color: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        /* Input field */
        .stTextInput input {
            border-radius: 8px !important;
            padding: 12px 14px !important;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #666;
            font-size: 0.9em;
            margin-top: 2rem;
            border-top: 1px solid #eee;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header-container {
                padding: 1.5rem 1rem;
            }
            
            .stButton>button {
                padding: 0.5rem 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Configure Gemini AI (use your actual API key)
genai.configure(api_key="AIzaSyClwCo8aIpV8gieeDQ5HsjiASODhGkxt-0")

# Model configuration (identical to your Flask version)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="pediatrician work\nFor example if i ask \"My child has cough for 3 days \" means it should reply like it cold disease \nand give some common medicin names and it should give generic answers not in depth\n\n",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your pediatric health assistant. How can I help?"}
    ]

# Set page config
st.set_page_config(
    page_title="Pediatric Health Assistant", 
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)
local_css()

# Header with gradient
st.markdown("""
<div class="header-container">
    <h1 style="margin:0;padding:0;">👶 Pediatric Health Assistant</h1>
    <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">Get quick pediatric advice for your child's health concerns</p>
</div>
""", unsafe_allow_html=True)

# Introduction card
st.markdown("""
<div class="card">
    <p>This assistant provides general pediatric health information. You can either type your question or use voice input.</p>
    <p><strong>Remember:</strong> This is not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👨‍⚕️" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Function to process voice input with better UX
def voice_input():
    recognizer = sr.Recognizer()
    with st.status("🎤 Listening... Speak now", expanded=True) as status:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Recognizing the speech
                try:
                    prompt = recognizer.recognize_google(audio)
                    status.update(label="✅ Voice captured", state="complete", expanded=False)
                    st.success(f"You said: {prompt}")
                    return prompt
                except sr.UnknownValueError:
                    status.update(label="❌ Couldn't understand audio", state="error", expanded=False)
                    st.error("Sorry, I could not understand the audio. Please try again.")
                    return None
                except sr.RequestError as e:
                    status.update(label="❌ Service error", state="error", expanded=False)
                    st.error(f"Could not request results from Google Speech Recognition service; {e}")
                    return None
        except Exception as e:
            status.update(label="❌ Microphone error", state="error", expanded=False)
            st.error(f"Error accessing microphone: {e}")
            return None

# Options for input: Text or Voice with better styling
input_mode = st.radio(
    "Choose your input method:",
    ("Text", "Voice"),
    horizontal=True,
    label_visibility="collapsed"
)

if input_mode == "Text":
    if prompt := st.chat_input("Ask about your child's symptoms..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message with typing animation effect
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Display assistant response with spinner
        with st.chat_message("assistant", avatar="👨‍⚕️"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("Analyzing your question..."):
                try:
                    # Simulate typing effect
                    response = model.generate_content(prompt)
                    for chunk in response.text.split(" "):
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif input_mode == "Voice":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎤 Click to Speak", use_container_width=True):
            prompt = voice_input()
            if prompt:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Display user message
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                
                # Display assistant response
                with st.chat_message("assistant", avatar="👨‍⚕️"):
                    with st.spinner("Analyzing your question..."):
                        try:
                            response = model.generate_content(prompt)
                            st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

# Navigation button with consistent styling
st.markdown("---")
if st.button("Detailed Symptom Checker", type="primary", use_container_width=True):
    st.switch_page("pages/trial.py")

# Footer
st.markdown("""
<div class="footer">
    <p>This tool is for informational purposes only and does not provide medical advice.</p>
    <p>Always consult a qualified healthcare provider for diagnosis and treatment.</p>
</div>
""", unsafe_allow_html=True)