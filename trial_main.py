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
from transformers import BertTokenizer, BertForMaskedLM
import torch
import time

# Set page config
st.set_page_config(
    page_title="Pediatric Health Assistant", 
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)


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

# Load alternative clinical model and tokenizer with caching
@st.cache_resource  # This caches the model and tokenizer
def load_clinical_model():
    tokenizer = BertTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    clinical_model = BertForMaskedLM.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    return tokenizer, clinical_model

tokenizer, clinical_model = load_clinical_model()

# Model configuration for Generative AI
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
    system_instruction="""
You are a helpful and friendly pediatrician chatbot designed to assist parents with common child health concerns.
Your responsibilities:
 - Answer questions related to common symptoms in children such as cold, cough, fever, stomach pain, rashes, vomiting, etc.
 - Provide general explanations for possible causes in simple and reassuring language.
 - Suggest commonly used over-the-counter (OTC) medications, only by generic names (e.g., paracetamol, cetirizine).
 - Mention age-appropriateness or dosage ranges when necessary, but avoid giving exact dosages.
 - Recommend seeing a pediatrician for persistent, severe, or unclear symptoms.
 - Keep answers brief, clear, and non-technical.
 - Avoid giving deep medical advice, prescription-level detail, or suggesting specific brands.

 Example:
 User: My child has had a cough for 3 days.
 You: It sounds like your child might have a common cold or viral infection, which often causes cough. Make sure they get enough fluids and rest. You can consider giving a children's cough syrup with a mild antihistamine like cetirizine. If the cough worsens or lasts more than a week, it's best to see a pediatrician.

 Always include a gentle reminder to consult a doctor for personalized care.
"""
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your pediatric health assistant. How can I help?"}
    ]

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

# Function to process voice input
def voice_input():
    recognizer = sr.Recognizer()
    with st.status("🎤 Listening... Speak now", expanded=True) as status:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                prompt = recognizer.recognize_google(audio)
                status.update(label="✅ Voice captured", state="complete", expanded=False)
                st.success(f"You said: {prompt}")
                return prompt
        except Exception as e:
            st.error(f"Error accessing microphone: {e}")
            return None

# Function to analyze input with Clinical BERT
def clinical_bert_query(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    with torch.no_grad():
        outputs = clinical_model(**inputs)
    # You can implement additional processing based on the outputs if required
    return prompt  # Here we're just passing the prompt, but you can modify as needed

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👨‍⚕️" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Options for input: Text or Voice
input_mode = st.radio(
    "Choose your input method:",
    ("Text", "Voice"),
    horizontal=True,
    label_visibility="collapsed"
)

if input_mode == "Text":
    if prompt := st.chat_input("Ask about your child's symptoms..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Analyze input with Clinical BERT
        clinical_response = clinical_bert_query(prompt)

        # Generate response from Google Model
        with st.chat_message("assistant", avatar="👨‍⚕️"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Analyzing your question..."):
                try:
                    response = model.generate_content(clinical_response)
                    for chunk in response.text.split(" "):
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif input_mode == "Voice":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎤 Click to Speak", use_container_width=True):
            prompt = voice_input()
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                
                # Analyze input with Clinical BERT
                clinical_response = clinical_bert_query(prompt)

                # Generate response from Google Model
                with st.chat_message("assistant", avatar="👨‍⚕️"):
                    with st.spinner("Analyzing your question..."):
                        try:
                            response = model.generate_content(clinical_response)
                            st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

# Navigation button
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
