import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")

# Configure the Gemini model
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")

# Minimum content length requirement
MIN_CONTENT_LENGTH = 60

def optimize_instagram_post(post_content, target_audience, theme, tone, hashtag_count):
    """
    Optimize Instagram post based on selected parameters
    """
    if not post_content.strip():
        return "Please enter some content to optimize."
    
    try:
        prompt = f"""
        Optimize the following Instagram post while maintaining its authentic voice:
        
        {post_content}
        
        Please enhance it based on these specifications:
        1. Target audience: {target_audience}
        2. Content theme: {theme}
        3. Tone of voice: {tone}
        4. Include exactly {hashtag_count} relevant hashtags
        5. Include a natural call-to-action
        6. Make it engaging while preserving the original message
        7. Keep it within Instagram's character limits
        8. Create a comprehensive and detailed post (at least 3-4 paragraphs)
        
        Return only the optimized post, don't explain your changes.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def optimize_edited_post(original_post, optimized_post, edit_instructions, target_audience, theme, tone, hashtag_count):
    """
    Re-optimize a post based on specific edit instructions
    """
    try:
        prompt = f"""
        I need to improve an Instagram post based on specific feedback.
        
        ORIGINAL USER POST:
        {original_post}
        
        CURRENT OPTIMIZED VERSION:
        {optimized_post}
        
        EDIT INSTRUCTIONS FROM USER:
        {edit_instructions}
        
        Please create a new optimized version with these specifications:
        1. Target audience: {target_audience}
        2. Content theme: {theme}
        3. Tone of voice: {tone}
        4. Include exactly {hashtag_count} relevant hashtags
        5. Include a natural call-to-action
        6. Make it engaging while preserving the original message
        7. Keep it within Instagram's character limits
        8. Create a comprehensive and detailed post (at least 3-4 paragraphs)
        9. Focus specifically on addressing the edit instructions
        
        Return only the re-optimized post, don't explain your changes.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="Think why? Post Helper",
        page_icon="📱",
        layout="wide"
    )
    
    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None
    
    if "edit_content" not in st.session_state:
        st.session_state.edit_content = ""
        
    if "edit_instructions" not in st.session_state:
        st.session_state.edit_instructions = ""
        
    if "original_content" not in st.session_state:
        st.session_state.original_content = ""
        
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
        
    if "reset_form" not in st.session_state:
        st.session_state.reset_form = False
        
    # Handle session state reset - moved to beginning of app flow
    if st.session_state.reset_form:
        # Reset the form-related session states 
        # Using dict update to avoid direct assignment to widget keys
        updated_state = {
            "editing_index": None,
            "reset_form": False
        }
        st.session_state.update(updated_state)
        
    # Custom CSS
    st.markdown("""
    <style>
    /* Global styling */
    .main {
        padding: 1.5rem;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        background-attachment: fixed;
        color: white;
    }
    
    /* Glassmorphism effects */
    .chat-container {
        margin-bottom: 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Message styling */
    .user-message {
        background: rgba(9, 99, 235, 0.15);
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border-left: 3px solid #0963eb;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    .bot-message {
        background: rgba(101, 219, 168, 0.15);
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border-left: 3px solid #65dba8;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        position: relative;
    }
    
    /* Message action buttons */
    .message-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .action-button {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .action-button:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #65dba8 0%, #0963eb 100%);
        color: white;
        font-weight: bold;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
    }
    
    /* Copy button styling */
    .copy-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.2);
        border: none;
        border-radius: 4px;
        color: white;
        padding: 5px 10px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
        z-index: 10;
    }
    
    .copy-btn:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Error message styling */
    .error-message {
        background-color: rgba(255, 87, 87, 0.2);
        color: #ff5757;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 3px solid #ff5757;
        margin-bottom: 1rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    .stTextArea textarea:focus {
        border-color: #65dba8;
        box-shadow: 0 0 0 2px rgba(101, 219, 168, 0.2);
    }
    
    /* Header styling */
    h1 {
        color: white;
        font-size: 2.4rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 0 0 10px 10px;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
        color: white;
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        backdrop-filter: blur(7px);
        -webkit-backdrop-filter: blur(7px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Label styling */
    label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Text and link styling */
    p, li {
        color: rgba(255, 255, 255, 0.9);
    }
    
    a {
        color: #65dba8 !important;
        text-decoration: none !important;
    }
    
    a:hover {
        text-decoration: underline !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Dropdown styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #65dba8 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # JavaScript for copy to clipboard functionality - fixed implementation
    st.components.v1.html("""
    <script>
    // Wait for the page to fully load
    document.addEventListener('DOMContentLoaded', function() {
        // Add click event listeners to all copy buttons
        document.querySelectorAll('.copy-btn').forEach(function(button) {
            button.addEventListener('click', function() {
                const contentId = this.getAttribute('data-content-id');
                const contentElement = document.getElementById(contentId);
                if (contentElement) {
                    navigator.clipboard.writeText(contentElement.innerText)
                    .then(() => {
                        const originalText = this.innerText;
                        this.innerText = 'Copied!';
                        setTimeout(() => {
                            this.innerText = originalText;
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy: ', err);
                    });
                }
            });
        });
    });

    // Function for dynamic elements added after page load
    function copyPostContent(id) {
        const content = document.getElementById(id).innerText;
        navigator.clipboard.writeText(content)
        .then(() => {
            const btn = document.querySelector(`[data-content-id="${id}"]`);
            if (btn) {
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                setTimeout(() => {
                    btn.innerText = originalText;
                }, 2000);
            }
        })
        .catch(err => {
            console.error('Failed to copy: ', err);
        });
        return false; // Prevent default action
    }
    </script>
    """, height=0)
    
    # App header
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-right: 1rem; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);">📱</div>
        <div>
            <h1 style="margin: 0; padding: 0;">Instagram Post Optimizer</h1>
            <p style="margin: 0; padding: 0; font-size: 1.1rem; opacity: 0.9;">Enhance your content for maximum engagement</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Function to handle edit requests
    def edit_message(index):
        if index > 0 and index % 2 == 1:  # This is an AI response
            user_index = index - 1
            if user_index >= 0:
                original_post = st.session_state.chat_history[user_index]["content"]
                st.session_state.original_content = original_post
        
        message = st.session_state.chat_history[index]
        st.session_state.editing_index = index
        # Don't set edit_content directly since it's now a widget key
        # Instead, use a separate initialization key
        st.session_state["temp_edit_content"] = message["content"]
    
    # Function to save edits - modified to use session state safely
    def save_edit(edit_content, edit_instructions, target_audience, theme, tone, hashtag_count):
        if st.session_state.editing_index is not None:
            if st.session_state.editing_index % 2 == 1:  # This is an AI response
                # Get the original user post
                user_index = st.session_state.editing_index - 1
                original_post = st.session_state.chat_history[user_index]["content"]
                
                # Generate a new optimized version based on edit instructions
                new_optimized_post = optimize_edited_post(
                    original_post, 
                    edit_content, 
                    edit_instructions,
                    target_audience,
                    theme,
                    tone,
                    hashtag_count
                )
                
                st.session_state.chat_history[st.session_state.editing_index]["content"] = new_optimized_post
            else:
                # This is a user message
                st.session_state.chat_history[st.session_state.editing_index]["content"] = edit_content
            
            # Signal to reset the form on next rerun instead of directly modifying widget keys
            st.session_state.reset_form = True
            
    # Display any error messages
    if st.session_state.error_message:
        st.markdown(f'<div class="error-message">{st.session_state.error_message}</div>', unsafe_allow_html=True)
        st.session_state.error_message = None
    
    # Display chat history
    if st.session_state.chat_history:
        with st.container():
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    # Create a unique ID for each message
                    message_id = f"message_{i}"
                    
                    # Add optimized post with copy button using HTML/JS approach
                    st.markdown(
                        f'''
                        <div class="bot-message">
                            <div id="{message_id}">{message["content"]}</div>
                            <button class="copy-btn" onclick="copyPostContent('{message_id}')">Copy</button>
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                    
                    # Add edit button for optimized posts
                    col1, col2 = st.columns([1, 9])
                    with col1:
                        if st.button("Edit", key=f"edit_{i}"):
                            edit_message(i)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Edit form (shown only when editing)
    if st.session_state.editing_index is not None:
        with st.form(key="edit_form"):
            st.subheader("Edit Content")
            
            # Show different form elements based on whether we're editing a user message or AI response
            if st.session_state.editing_index % 2 == 1:  # This is an AI response
                # Use the temp value for initial content if available
                initial_content = st.session_state.get("temp_edit_content", 
                                   st.session_state.chat_history[st.session_state.editing_index]["content"])
                
                edit_content = st.text_area("Current Optimized Content", 
                                           value=initial_content, 
                                           height=150, 
                                           key="edit_content")
                
                edit_instructions = st.text_area("Edit Instructions (What would you like to change?)", 
                                  placeholder="e.g., 'Make it more casual', 'Add more details about pricing', 'Focus more on sustainability'", 
                                  height=100, 
                                  key="edit_instructions")
                
                # Show customization options for the re-optimization
                col1, col2 = st.columns(2)
                with col1:
                    target_audience = st.selectbox(
                        "Target Audience", 
                        options=["General", "Teenagers", "Young Adults", "Professionals", "Parents", "Seniors", 
                                "Business Owners", "Travel Enthusiasts", "Health & Fitness", "Tech Enthusiasts", 
                                "Fashion Enthusiasts", "Foodies"],
                        key="edit_target_audience"
                    )
                    
                    theme = st.selectbox(
                        "Content Theme",
                        options=["General", "Lifestyle", "Travel", "Food", "Fashion", "Beauty", "Fitness", 
                                "Business", "Education", "Technology", "Entertainment", "Motivation"],
                        key="edit_theme"
                    )
                
                with col2:
                    tone = st.selectbox(
                        "Tone of Voice",
                        options=["Professional", "Casual", "Friendly", "Authoritative", "Inspirational", 
                                "Humorous", "Serious", "Conversational", "Enthusiastic", "Informative"],
                        key="edit_tone"
                    )
                    
                    hashtag_count = st.selectbox(
                        "Number of Hashtags",
                        options=list(range(1, 31)),
                        index=9,  # Default to 10 hashtags
                        key="edit_hashtag_count"
                    )
                
                submit_edit = st.form_submit_button("Re-Optimize Post")
                if submit_edit:
                    if edit_instructions:
                        save_edit(
                            edit_content,
                            edit_instructions,
                            target_audience,
                            theme,
                            tone,
                            hashtag_count
                        )
                        st.rerun()
                    else:
                        st.session_state.error_message = "Please provide edit instructions to explain what you'd like to change."
                        st.rerun()
            else:
                # Editing a user message
                # Use the temp value for initial content if available
                initial_content = st.session_state.get("temp_edit_content", 
                                   st.session_state.chat_history[st.session_state.editing_index]["content"])
                
                edit_content = st.text_area("Edit your post", 
                                           value=initial_content, 
                                           height=150, 
                                           key="edit_content")
                
                submit_edit = st.form_submit_button("Save Changes")
                if submit_edit:
                    if len(edit_content.strip()) < MIN_CONTENT_LENGTH:
                        st.session_state.error_message = f"Please provide more detailed content (at least {MIN_CONTENT_LENGTH} characters)."
                        st.rerun()
                    else:
                        save_edit(edit_content, "", "", "", "", "")
                        st.rerun()
    
    # Content customization options and input form
    with st.form(key="post_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            target_audience = st.selectbox(
                "Target Audience", 
                options=["General", "Teenagers", "Young Adults", "Professionals", "Parents", "Seniors", 
                        "Business Owners", "Travel Enthusiasts", "Health & Fitness", "Tech Enthusiasts", 
                        "Fashion Enthusiasts", "Foodies"]
            )
            
            theme = st.selectbox(
                "Content Theme",
                options=["General", "Lifestyle", "Travel", "Food", "Fashion", "Beauty", "Fitness", 
                        "Business", "Education", "Technology", "Entertainment", "Motivation"]
            )
        
        with col2:
            tone = st.selectbox(
                "Tone of Voice",
                options=["Professional", "Casual", "Friendly", "Authoritative", "Inspirational", 
                        "Humorous", "Serious", "Conversational", "Enthusiastic", "Informative"]
            )
            
            hashtag_count = st.selectbox(
                "Number of Hashtags",
                options=list(range(1, 31)),
                index=9  # Default to 10 hashtags
            )
        
        user_input = st.text_area(
            "Paste your Instagram post here:",
            height=150,
            placeholder=f"Type or paste your Instagram post content here (minimum {MIN_CONTENT_LENGTH} characters)..."
        )
        
        submit_button = st.form_submit_button("✨ Optimize Post")
    
    # Process the post when submitted
    if submit_button:
        if not user_input or len(user_input.strip()) < MIN_CONTENT_LENGTH:
            st.session_state.error_message = f"Please provide more detailed content (at least {MIN_CONTENT_LENGTH} characters) for better optimization results."
            st.rerun()
        else:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get optimized post
            with st.spinner("Optimizing your post..."):
                optimized_post = optimize_instagram_post(user_input, target_audience, theme, tone, hashtag_count)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": optimized_post})
            
            # Rerun to update the UI with new messages
            st.rerun()
    

if __name__ == "__main__":
    main()
