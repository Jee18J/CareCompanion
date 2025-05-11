# import streamlit as st
# import json
# import os
# from datetime import datetime

# # Main UI
# st.set_page_config(page_title="Parent Forum", layout="wide")


# # Load condition list from model prediction classes
# CONDITIONS = [
#     "Common Cold", "Gastroenteritis", "Asthma", "Meningitis",
#     "Scarlet Fever", "Eczema", "Croup", "Type 1 Diabetes",
#     "Bronchiolitis", "Influenza", "Pneumonia",
#     "Allergies", "Ear Infection", "Skin Rash", "Diarrhea", "Fever", "Viral Illness"
# ]

# DATA_FILE = "pages/questions.json"

# # Initialize data file if not exists
# def load_data():
#     """Loads forum data from the JSON file."""
#     if not os.path.exists(DATA_FILE):
#         with open(DATA_FILE, 'w') as f:
#             json.dump({}, f)
#     try:
#         with open(DATA_FILE, 'r') as f:
#             data = json.load(f)
#             if not isinstance(data, dict):
#                 st.error(f"Data file {DATA_FILE} is corrupted. Resetting.")
#                 data = {}
#                 save_data(data)
#             # Ensure each question has an 'answers' list and each answer has 'votes'
#             for condition, questions in data.items():
#                 for q in questions:
#                     if 'answers' not in q:
#                         q['answers'] = []
#                     for ans in q['answers']:
#                         if 'votes' not in ans:
#                             ans['votes'] = 0
#             return data
#     except json.JSONDecodeError:
#         st.error(f"Error decoding JSON from {DATA_FILE}. File might be corrupted. Resetting.")
#         data = {}
#         save_data(data)
#         return data
#     except Exception as e:
#         st.error(f"An error occurred loading data: {e}")
#         data = {}
#         save_data(data)
#         return data

# def save_data(data):
#     """Saves forum data to the JSON file."""
#     try:
#         with open(DATA_FILE, 'w') as f:
#             json.dump(data, f, indent=4)
#     except Exception as e:
#         st.error(f"An error occurred saving data: {e}")

# # Format helper
# def format_question_id(condition, title):
#     """Creates a unique ID for a question."""
#     # Using a timestamp ensures uniqueness even if questions have similar titles
#     timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S%f") # Add microseconds for higher uniqueness

#     # Perform the replace operations *before* the f-string
#     cleaned_title = title[:50].strip().replace(' ', '_').replace('/', '_').replace('\\', '_')

#     return f"{condition}___{cleaned_title}___{timestamp_str}"

# def format_answer_id():
#      """Creates a unique ID for an answer."""
#      return datetime.now().strftime("%Y%m%d%H%M%S%f") # Use timestamp for answer ID


# # Custom CSS for the + button and form styling
# st.markdown("""
# <style>
# .create-question-button {
#     position: fixed;
#     top: 20px;
#     right: 20px;
#     z-index: 1000;
# }

# .stButton>button {
#     font-size: 1.2em;
#     padding: 10px 15px;
#     border-radius: 50%;
#     width: 50px;
#     height: 50px;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
#     /* Adjust button color for plus if needed */
#     /* background-color: #4CAF50; */
#     /* color: white; */
# }

# /* Style for the create question form container */
# .create-question-form-container {
#     border: 1px solid #d3d3d3; /* Light gray border */
#     padding: 20px;
#     border-radius: 5px;
#     margin-bottom: 20px; /* Space below the form */
#     background-color: #f9f9f9; /* Light background */
# }

# /* Style for scrollable question list (optional, within expander) */
# .scrollable-questions {
#     max-height: 400px; /* Set a max height */
#     overflow-y: auto; /* Add scrollbar when content exceeds max height */
#     padding-right: 15px; /* Add some padding for the scrollbar */
# }

# /* Style for answer container */
# .answer-container {
#     border-top: 1px solid #eee; /* Light border above answers */
#     margin-top: 10px;
#     padding-top: 10px;
#     padding-left: 10px; /* Indent answers slightly */
#     background-color: #ffffff; /* White background for answers */
#     border-radius: 5px;
#     margin-bottom: 5px; /* Space between answers */
#     box-shadow: 1px 1px 5px rgba(0,0,0,0.05); /* Subtle shadow */
# }

# .answer-votes {
#     font-weight: bold;
#     margin-right: 10px;
#     color: #333;
# }

# .vote-buttons button {
#     font-size: 0.8em;
#     padding: 2px 5px;
#     margin-right: 5px;
#     width: auto; /* Override the 50px width from the main button style */
#     height: auto;
#     border-radius: 3px;
#     box-shadow: none; /* Remove shadow from small buttons */
# }

# </style>
# """, unsafe_allow_html=True)


# # --- Load Data ---
# data = load_data()

# # Use columns to place title and the + button side-by-side
# col_title, col_plus = st.columns([10, 1]) # Adjust column width ratio as needed

# with col_title:
#     st.title("👪 Parent Forum - Ask & Share")

# with col_plus:
#     # Using session state to control the visibility of the "create question" form
#     if 'show_create_question' not in st.session_state:
#         st.session_state.show_create_question = False

#     # Button to toggle the create question form visibility (positioned via CSS)
#     # The actual button is placed here, but the CSS moves it
#     if st.button("➕", key="create_question_toggle"):
#         st.session_state.show_create_question = not st.session_state.show_create_question
#         st.rerun() # Rerun to make the form appear/disappear

# # --- Question Posting Form (Conditional Display) ---
# # Display the create question form if session state is True
# if st.session_state.show_create_question:
#     st.markdown("### ➕ Create New Question")
#     # Apply custom CSS class to the container
#     with st.container():
#         st.markdown('<div class="create-question-form-container">', unsafe_allow_html=True)
#         selected_condition_post = st.selectbox("Select Condition", options=CONDITIONS, key="new_q_condition")
#         new_question = st.text_area("Your Question", key="new_q_text")
#         col_post_buttons = st.columns([1, 1, 4]) # Use columns for buttons

#         with col_post_buttons[0]:
#             if st.button("Post", type="primary"):
#                 if selected_condition_post and new_question.strip():
#                     if selected_condition_post not in data:
#                         data[selected_condition_post] = []

#                     question_entry = {
#                         "id": format_question_id(selected_condition_post, new_question),
#                         "question": new_question.strip(), # Strip whitespace
#                         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
#                         "answers": [] # Initialize with an empty list for answers
#                     }
#                     data[selected_condition_post].append(question_entry)
#                     save_data(data)
#                     st.success("Question posted!")
#                     # Optionally hide the form after posting
#                     st.session_state.show_create_question = False
#                     st.rerun() # Rerun to display the new question
#                 else:
#                     st.warning("Please fill both fields.")
#         with col_post_buttons[1]:
#             if st.button("Cancel"):
#                 st.session_state.show_create_question = False
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True) # Close the custom div

# st.markdown("---") # Separator after the potential question form

# # --- Browse and Display Questions ---
# st.header("🔍 Browse Questions by Condition")

# selected_category_browse = st.selectbox(
#     "Select a condition to view questions",
#     options=["Select a Condition"] + sorted(list(data.keys())),
#     key="browse_category"
# )

# st.markdown("---")

# # --- Display Questions and Answers for Selected Category ---
# if selected_category_browse != "Select a Condition":
#     condition_to_display = selected_category_browse
#     questions = data.get(condition_to_display, [])

#     if questions:
#         st.markdown(f"### 🩺 Questions about {condition_to_display}")
#         st.markdown('<div class="scrollable-questions">', unsafe_allow_html=True)

#         # Loop through questions for the selected condition
#         for i, q in enumerate(questions):
#             # Use question ID for unique expander key
#             expander_key = f"expander_{q['id']}"
#             with st.expander(f"**{q['question']}**", expanded=st.session_state.get(expander_key, False)):
#                 st.caption(f"Posted on: {q['timestamp']}")

#                 # --- Display Answers ---
#                 st.markdown("#### Answers:")
#                 if q['answers']:
#                     # Sort answers by votes in descending order
#                     sorted_answers = sorted(q['answers'], key=lambda ans: ans.get('votes', 0), reverse=True)
#                     # Display top N answers (e.g., top 5)
#                     top_n_answers = sorted_answers[:5] # Adjust N here

#                     for j, ans in enumerate(top_n_answers):
#                          # Use answer ID for unique keys within the answer section
#                          answer_key_prefix = f"answer_{ans.get('id', j)}_{i}" # Use answer ID if available, fallback to index+q_index

#                          st.markdown('<div class="answer-container">', unsafe_allow_html=True)
#                          st.write(ans['answer'])
#                          st.caption(f"Answered on: {ans['timestamp']}")

#                          # Voting buttons and vote count
#                          col_votes, col_upvote, col_downvote = st.columns([1, 1, 10])
#                          with col_votes:
#                              st.markdown(f'<span class="answer-votes">{ans.get("votes", 0)} votes</span>', unsafe_allow_html=True)

#                          with col_upvote:
#                              # Unique key for upvote button
#                              if st.button("👍", key=f"{answer_key_prefix}_upvote"):
#                                  ans['votes'] = ans.get('votes', 0) + 1
#                                  save_data(data)
#                                  st.rerun() # Rerun to update vote count and sorting

#                          with col_downvote:
#                             # Unique key for downvote button
#                              if st.button("👎", key=f"{answer_key_prefix}_downvote"):
#                                  ans['votes'] = ans.get('votes', 0) - 1
#                                  save_data(data)
#                                  st.rerun() # Rerun to update vote count and sorting

#                          st.markdown('</div>', unsafe_allow_html=True) # Close answer container div

#                     if len(sorted_answers) > 5:
#                         st.info(f"Showing top 5 answers. Total answers: {len(sorted_answers)}") # Indicate if more answers exist

#                 else:
#                     st.info("No answers yet. Be the first to answer!")

#                 # --- Post an Answer Form ---
#                 st.markdown("---")
#                 st.markdown("##### Post an Answer:")
#                 # Use question ID for unique key for the answer text area
#                 new_answer_text = st.text_area("Your Answer", key=f"answer_text_{q['id']}")
#                 # Use question ID for unique key for the post answer button
#                 if st.button("Post Answer", key=f"post_answer_button_{q['id']}"):
#                     if new_answer_text.strip():
#                         answer_entry = {
#                             "id": format_answer_id(), # Generate unique ID for answer
#                             "answer": new_answer_text.strip(), # Strip whitespace
#                             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
#                             "votes": 0 # Initialize votes to 0
#                         }
#                         q['answers'].append(answer_entry) # Add answer to the question's answers list
#                         save_data(data)
#                         st.success("Answer posted!")
#                         # Clear the text area and rerun to display the new answer
#                         st.session_state[f"answer_text_{q['id']}"] = "" # Clear the text area
#                         st.rerun()
#                     else:
#                         st.warning("Please enter your answer.")

#         st.markdown('</div>', unsafe_allow_html=True) # Close the scrollable div
#     else:
#          st.info(f"No questions posted yet for '{condition_to_display}'. Be the first to ask!")

# else:
#     st.info("Select a condition from the dropdown above to view related questions.")


# # --- Footer (Optional) ---
# st.markdown("---")
# st.markdown("Forum powered by Streamlit & JSON")



#working

# import streamlit as st
# import json
# import os
# from datetime import datetime

# # Main UI
# st.set_page_config(page_title="Parent Forum Blog", layout="wide")

# # --- Load condition list from model prediction classes ---
# CONDITIONS = [
#     "Common Cold", "Gastroenteritis", "Asthma", "Meningitis",
#     "Scarlet Fever", "Eczema", "Croup", "Type 1 Diabetes",
#     "Bronchiolitis", "Influenza", "Pneumonia",
#     "Allergies", "Ear Infection", "Skin Rash", "Diarrhea", "Fever", "Viral Illness" # Added back some conditions
# ]

# # --- Data File ---
# DATA_FILE = "pages/blogs.json"

# # --- Helper Functions ---
# def load_data():
#     """Loads forum data from the JSON file."""
#     if not os.path.exists(DATA_FILE):
#         # Initialize with an empty dictionary
#         with open(DATA_FILE, 'w') as f:
#             json.dump({}, f)
#     try:
#         with open(DATA_FILE, 'r') as f:
#             data = json.load(f)
#             # Ensure the loaded data is a dictionary
#             if not isinstance(data, dict):
#                 st.error(f"Data file {DATA_FILE} is corrupted or not a dictionary. Resetting.")
#                 data = {}
#                 save_data(data)
#             # Ensure each condition entry is a list
#             for condition in CONDITIONS:
#                  if condition not in data:
#                       data[condition] = []
#                  elif not isinstance(data[condition], list):
#                       st.error(f"Data for condition '{condition}' is corrupted or not a list. Resetting.")
#                       data[condition] = []
#             return data
#     except json.JSONDecodeError:
#         st.error(f"Error decoding JSON from {DATA_FILE}. File might be corrupted. Resetting.")
#         data = {}
#         save_data(data)
#         return data
#     except Exception as e:
#         st.error(f"An error occurred loading data: {e}")
#         data = {}
#         save_data(data)
#         return data


# def save_data(data):
#     """Saves forum data to the JSON file."""
#     try:
#         with open(DATA_FILE, 'w') as f:
#             json.dump(data, f, indent=4)
#     except Exception as e:
#         st.error(f"An error occurred saving data: {e}")

# # Format blog ID
# def format_blog_id(condition, title):
#     """Creates a unique ID for a blog post."""
#     # Using a timestamp ensures uniqueness even if titles are similar
#     timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S%f") # Add microseconds for higher uniqueness

#     # Clean the title for use in the ID
#     # Limit length and replace problematic characters
#     cleaned_title = title[:50].strip().replace(' ', '_').replace('/', '_').replace('\\', '_').replace('.', '_').replace(':', '_')

#     return f"{condition}___{cleaned_title}___{timestamp_str}"


# # --- Custom CSS for the + button and form styling ---
# st.markdown("""
# <style>
# .create-post-button {
#     position: fixed;
#     top: 20px;
#     right: 20px;
#     z-index: 1000;
# }

# .stButton>button {
#     font-size: 1.2em;
#     padding: 10px 15px;
#     border-radius: 50%;
#     width: 50px;
#     height: 50px;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
# }

# /* Style for the create post form container */
# .create-post-form-container {
#     border: 1px solid #d3d3d3; /* Light gray border */
#     padding: 20px;
#     border-radius: 5px;
#     margin-bottom: 20px; /* Space below the form */
#     background-color: #f9f9f9; /* Light background */
# }

# /* Style for scrollable blog list (optional) */
# .scrollable-blogs {
#     max-height: 600px; /* Set a max height */
#     overflow-y: auto; /* Add scrollbar when content exceeds max height */
#     padding-right: 15px; /* Add some padding for the scrollbar */
# }

# /* Style for individual blog post container */
# /* Removed the main border as expander adds one */
# /* .blog-post-container {
#     margin-top: 15px;
#     padding: 15px;
#     background-color: #ffffff;
#     border-radius: 5px;
#     box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
# } */

# .blog-post-title {
#     margin-bottom: 5px;
# }

# .blog-post-timestamp {
#     font-size: 0.8em;
#     color: gray;
#     margin-bottom: 10px;
# }

# /* Style for the content within the expander */
# .expander-content {
#     padding-top: 10px;
#     border-top: 1px solid #eee; /* Separator above content */
#     margin-top: 10px;
# }

# </style>
# """, unsafe_allow_html=True)


# # --- Load Data ---
# data = load_data()

# # --- Title and Create Post Button ---
# col_title, col_plus = st.columns([10, 1]) # Adjust column width ratio as needed

# with col_title:
#     st.title("📝 Parent Forum Blog - Share Your Experiences")

# with col_plus:
#     # Using session state to control the visibility of the "create post" form
#     if 'show_create_post' not in st.session_state:
#         st.session_state.show_create_post = False

#     # Button to toggle the create post form visibility (positioned via CSS)
#     if st.button("➕", key="create_post_toggle"):
#         st.session_state.show_create_post = not st.session_state.show_create_post
#         st.rerun() # Rerun to make the form appear/disappear

# # --- Blog Posting Form (Conditional Display) ---
# # Display the create post form if session state is True
# if st.session_state.show_create_post:
#     st.markdown("### ➕ Share a New Blog Post")
#     # Apply custom CSS class to the container
#     with st.container():
#         st.markdown('<div class="create-post-form-container">', unsafe_allow_html=True)
#         selected_condition_post = st.selectbox("Select Condition", options=CONDITIONS, key="new_blog_condition")
#         new_blog_title = st.text_input("Blog Title", key="new_blog_title")
#         new_blog_content = st.text_area("Your Experience / Content", height=200, key="new_blog_content") # Added height

#         col_post_buttons = st.columns([1, 1, 4]) # Use columns for buttons

#         with col_post_buttons[0]:
#             if st.button("Post Blog", type="primary"):
#                 if selected_condition_post and new_blog_title.strip() and new_blog_content.strip():
#                     # Ensure the condition exists in data
#                     if selected_condition_post not in data:
#                         data[selected_condition_post] = []

#                     blog_entry = {
#                         "id": format_blog_id(selected_condition_post, new_blog_title),
#                         "title": new_blog_title.strip(),
#                         "content": new_blog_content.strip(),
#                         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
#                     }
#                     data[selected_condition_post].append(blog_entry)
#                     save_data(data)
#                     st.success("Blog post shared!")
#                     # Optionally hide the form after posting
#                     st.session_state.show_create_post = False
#                     st.rerun() # Rerun to display the new blog post
#                 else:
#                     st.warning("Please fill in the title and content.")
#         with col_post_buttons[1]:
#             if st.button("Cancel"):
#                 st.session_state.show_create_post = False
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True) # Close the custom div

# st.markdown("---") # Separator after the potential post form

# # --- Browse and Display Blogs ---
# st.header("📚 Browse Blog Posts by Condition")

# selected_category_browse = st.selectbox(
#     "Select a condition to view blog posts",
#     options=["Select a Condition"] + sorted(list(data.keys())),
#     key="browse_category"
# )

# st.markdown("---")

# # --- Display Blogs for Selected Category ---
# if selected_category_browse != "Select a Condition":
#     condition_to_display = selected_category_browse
#     blogs = data.get(condition_to_display, [])

#     if blogs:
#         st.markdown(f"### 🩺 Blog Posts about {condition_to_display}")
#         st.markdown('<div class="scrollable-blogs">', unsafe_allow_html=True)

#         # Loop through blog posts for the selected condition
#         # Display in reverse chronological order (newest first)
#         for blog in reversed(blogs):
#              # Use blog ID for unique expander key
#              expander_key = f"blog_expander_{blog['id']}"
#              # Use session state to control expander state persistence
#              if expander_key not in st.session_state:
#                   st.session_state[expander_key] = False # Default to collapsed

#              # Use st.expander with the blog title as the label
#              # The expanded state is controlled by session state
#              with st.expander(f"**{blog['title']}**", expanded=st.session_state[expander_key]):
#                  # Display timestamp and content inside the expander
#                  st.markdown(f'<p class="blog-post-timestamp">Posted on: {blog["timestamp"]}</p>', unsafe_allow_html=True)
#                  st.markdown('<div class="expander-content">', unsafe_allow_html=True) # Optional: Add container for padding/border
#                  st.markdown(blog['content']) # Use markdown to render content
#                  st.markdown('</div>', unsafe_allow_html=True) # Close expander content container


#         st.markdown('</div>', unsafe_allow_html=True) # Close the scrollable div
#     else:
#          st.info(f"No blog posts yet for '{condition_to_display}'. Be the first to share your experience!")

# else:
#     st.info("Select a condition from the dropdown above to view related blog posts.")


# # --- Footer (Optional) ---
# st.markdown("---")
# st.markdown("Blog Forum powered by Streamlit & JSON")




import streamlit as st
import json
import os
import uuid
import hashlib
from datetime import datetime

# Main UI configuration with custom theme
st.set_page_config(
    page_title="Parent Forum Blog",
    layout="wide",
    page_icon="👪",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better UI ---
def load_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background-color: #f9f9f9;
        }
        
        /* Header styling */
        .header {
            color: #2c3e50;
            padding: 1rem 0;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Blog post cards */
        .blog-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .blog-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .blog-title {
            color: #2c3e50;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .blog-meta {
            color: #7f8c8d;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }
        
        .blog-content {
            color: #34495e;
            line-height: 1.6;
        }
        
        /* Notification styling */
        .notification {
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0 4px 4px 0;
        }
        
        /* Form styling */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 8px !important;
            padding: 10px !important;
        }
        
        /* Condition selector */
        .stSelectbox>div>div>select {
            border-radius: 8px !important;
            padding: 8px !important;
        }
        
        /* Footer styling */
        .footer {
            color: #7f8c8d;
            font-size: 0.85rem;
            text-align: center;
            padding: 1.5rem 0;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .blog-card {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- Configuration ---
USERS_FILE = "pages/simulated_users.json"
BLOGS_FILE = "pages/blogs.json"
NOTIFICATIONS_FILE = "pages/simulated_blog_notifications.json"

# --- Load condition list from model prediction classes ---
CONDITIONS = [
    "Common Cold", "Gastroenteritis", "Asthma", "Meningitis",
    "Scarlet Fever", "Eczema", "Croup", "Type 1 Diabetes",
    "Bronchiolitis", "Influenza", "Pneumonia",
    "Allergies", "Ear Infection", "Skin Rash", "Diarrhea", "Fever", "Viral Illness"
]

# --- Helper Functions for Data Persistence ---
def load_data(filename, default_value):
    """Loads data from a JSON file."""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default_value, f)
        return default_value

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            if not isinstance(data, type(default_value)):
                st.error(f"Data file {filename} is corrupted or not the expected type. Resetting.")
                data = default_value
                save_data(data, filename)
            return data
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {filename}. File might be corrupted. Resetting.")
        data = default_value
        save_data(data, filename)
        return data
    except Exception as e:
        st.error(f"An error occurred loading data from {filename}: {e}")
        data = default_value
        save_data(data, filename)
        return data

def save_data(data, filename):
    """Saves data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"An error occurred saving data to {filename}: {e}")

# --- Simple Password Hashing (for simulation) ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, provided_password):
    return stored_hash == hash_password(provided_password)

# --- Load Data ---
users = load_data(USERS_FILE, {})
blogs_data = load_data(BLOGS_FILE, {})
notifications = load_data(NOTIFICATIONS_FILE, {})

# Ensure all conditions exist in blogs_data
for condition in CONDITIONS:
    if condition not in blogs_data:
        blogs_data[condition] = []
    elif not isinstance(blogs_data[condition], list):
        st.error(f"Data for condition '{condition}' in {BLOGS_FILE} is corrupted or not a list. Resetting.")
        blogs_data[condition] = []
        save_data(blogs_data, BLOGS_FILE)

# --- Initialize Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'show_create_post' not in st.session_state:
    st.session_state.show_create_post = False

# --- Authentication Logic ---
def login_form():
    with st.container():
        st.markdown('<div class="header"><h2>👋 Welcome Back</h2></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                login_submitted = st.form_submit_button("Login", type="primary")
            with col2:
                st.write("Don't have an account? Register below.")
            
            if login_submitted:
                if username in users:
                    if check_password(users[username]['password_hash'], password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = users[username]['user_id']
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("Username not found. Please register.")

def register_form():
    with st.container():
        st.markdown('<div class="header"><h2>✍️ Create an Account</h2></div>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            new_username = st.text_input("Choose a Username", key="register_username")
            new_password = st.text_input("Create a Password", type="password", key="register_password")
            
            register_submitted = st.form_submit_button("Register", type="primary")
            
            if register_submitted:
                if not new_username or not new_password:
                    st.warning("Please enter both a username and password.")
                elif new_username in users:
                    st.error("Username already exists. Please choose another.")
                else:
                    user_id = str(uuid.uuid4())
                    users[new_username] = {
                        'user_id': user_id,
                        'password_hash': hash_password(new_password)
                    }
                    save_data(users, USERS_FILE)
                    st.success("Registration successful! You can now log in.")

# --- Helper to get username from user_id ---
def get_username_from_userid(user_id):
    for username, user_info in users.items():
        if user_info.get('user_id') == user_id:
            return username
    return "Unknown User"

# --- Blog Content Display ---
def display_blog_post(blog, condition_to_display):
    with st.expander(f"📌 {blog['title']} - Posted on {blog['timestamp']} by {get_username_from_userid(blog['user_id'])}"):
        st.markdown(f'<div class="blog-content">{blog["content"]}</div>', unsafe_allow_html=True)
        
        # Report button for other users' posts
        if st.session_state.logged_in and st.session_state.user_id != blog['user_id']:
            if st.button("⚠️ Report This Post", key=f"report_post_{blog['id']}"):
                deleted_post_owner_id = blog['user_id']
                deleted_post_title = blog['title']
                deleted_post_id = blog['id']
                reported_by_username = st.session_state.username

                # Perform deletion
                blogs_data[condition_to_display] = [p for p in blogs_data[condition_to_display] if p['id'] != deleted_post_id]
                save_data(blogs_data, BLOGS_FILE)

                # Create notification
                poster_username = get_username_from_userid(deleted_post_owner_id)

                if poster_username:
                    notification_message = f"Your post '{deleted_post_title}' was reported and removed by {reported_by_username}."
                    notification_id = str(uuid.uuid4())

                    if poster_username not in notifications:
                        notifications[poster_username] = []

                    notifications[poster_username].append({
                        'id': notification_id,
                        'message': notification_message,
                        'read': False,
                        'user_id': deleted_post_owner_id
                    })
                    save_data(notifications, NOTIFICATIONS_FILE)

                    st.success(f"Post reported and removed. The original poster will be notified.")
                    st.rerun()
                else:
                    st.error("Could not find the original poster's username to send a notification.")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Blog and Notification Logic ---
def show_blog_content():
    # Header
    st.markdown('<div class="header"><h1>👪 Parent Forum Blog</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #7f8c8d;">Share your experiences and connect with other parents</p>', unsafe_allow_html=True)
    
    current_username = st.session_state.username
    current_user_id = st.session_state.user_id

    # Notifications section - CHANGED THIS PART
    if current_username in notifications:
        user_notifications = notifications[current_username]
        # Only show notifications where the current user is the intended recipient (user_id matches)
        unread_notifications = [n for n in user_notifications if not n['read']]

        if unread_notifications:
            st.markdown('<div class="header"><h3>🔔 Your Notifications</h3></div>', unsafe_allow_html=True)
            for notif in unread_notifications:
                with st.container():
                    st.markdown(f'<div class="notification">{notif["message"]}</div>', unsafe_allow_html=True)
                    if st.button("✔️ Mark as Read", key=f"close_notification_{notif['id']}"):
                        for existing_notif in notifications[current_username]:
                            if existing_notif['id'] == notif['id']:
                                existing_notif['read'] = True
                                break
                        save_data(notifications, NOTIFICATIONS_FILE)
                        st.rerun()

    col1, col2, col3 = st.columns([1, 2, 1])  # Creates a centered column
    with col1:
        pass
    with col2:
        if st.session_state.logged_in:
            if st.button("✍️ Create a New Post sharing you experiences", 
                         key="create_post_toggle",
                         use_container_width=True):
                st.session_state.show_create_post = not st.session_state.show_create_post
                st.rerun()
                with col3:
                    pass

    # Blog Posting Form
    if st.session_state.show_create_post and st.session_state.logged_in:
        with st.container():
            st.markdown('<div class="blog-card">', unsafe_allow_html=True)
            st.markdown('<h3>✏️ Create New Post</h3>', unsafe_allow_html=True)
            
            with st.form("new_post_form"):
                selected_condition_post = st.selectbox("Condition", options=CONDITIONS, key="new_blog_condition")
                new_blog_title = st.text_input("Post Title", key="new_blog_title")
                new_blog_content = st.text_area("Share Your Experience", height=200, key="new_blog_content")
                
                col_submit, col_cancel, _ = st.columns([1, 1, 4])
                with col_submit:
                    submit_post = st.form_submit_button("Publish Post", type="primary")
                with col_cancel:
                    cancel_post = st.form_submit_button("Cancel")
                
                if submit_post:
                    if selected_condition_post and new_blog_title.strip() and new_blog_content.strip():
                        if selected_condition_post not in blogs_data:
                            blogs_data[selected_condition_post] = []

                        blog_entry = {
                            "id": str(uuid.uuid4()),
                            "title": new_blog_title.strip(),
                            "content": new_blog_content.strip(),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "user_id": st.session_state.user_id
                        }
                        blogs_data[selected_condition_post].append(blog_entry)
                        save_data(blogs_data, BLOGS_FILE)
                        st.success("Your post has been published!")
                        st.session_state.show_create_post = False
                        st.rerun()
                    else:
                        st.warning("Please fill in both title and content.")
                
                if cancel_post:
                    st.session_state.show_create_post = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Blog Post Browser
    st.markdown('<div class="header"><h2>🔍 Browse Posts by Condition</h2></div>', unsafe_allow_html=True)
    
    selected_category_browse = st.selectbox(
        "Select a condition to view posts",
        options=["Select a Condition"] + sorted(list(blogs_data.keys())),
        key="browse_category"
    )

    st.markdown("---")

    # Display Blogs for Selected Category
    if selected_category_browse != "Select a Condition":
        condition_to_display = selected_category_browse
        blogs = blogs_data.get(condition_to_display, [])

        if blogs:
            st.markdown(f'<h3>🩺 Posts about {condition_to_display}</h3>', unsafe_allow_html=True)
            
            for blog in reversed(blogs):
                display_blog_post(blog, condition_to_display)
        else:
            st.info(f"No posts yet for '{condition_to_display}'. Be the first to share your experience!")
    else:
        st.info("Select a condition from the dropdown above to view related posts.")

    # Logout Button
    st.markdown("---")
    if st.session_state.logged_in:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.session_state.show_create_post = False
            st.success("Logged out successfully.")
            st.rerun()

# --- Main App Flow ---
if st.session_state.logged_in:
    show_blog_content()
else:
    # Splash page for non-logged-in users
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem;">
            <h1 style="color: #2c3e50;">👪 Welcome to Parent Forum</h1>
            <p style="color: #7f8c8d; font-size: 1.1rem;">
                A safe space for parents to share experiences, ask questions, 
                and support each other through childhood health journeys.
            </p>
            <p style="color: #7f8c8d; font-size: 1.1rem;">
                Join our community to connect with other parents facing similar challenges.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        login_form()
        st.markdown("---")
        register_form()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Parent Forum Blog | A community support platform</p>
    <p>Powered by Streamlit | All content is user-generated</p>
</div>
""", unsafe_allow_html=True)