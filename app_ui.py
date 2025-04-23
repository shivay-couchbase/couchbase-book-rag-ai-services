import streamlit as st
import base64
from pathlib import Path

# Couchbase branding
COUCHBASE_LOGO = "https://emoji.slack-edge.com/T024FJS4M/couchbase/4a361e948b15ed91.png"
COUCHBASE_COLORS = {
    "primary": "#EA0029",
    "secondary": "#1A1A1A",
    "background": "#F5F5F5",
    "text": "#333333"
}

def img_to_base64(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def init_ui():
    # Streamlit Page Configuration
    st.set_page_config(
        page_title="Couchbase Book Knowledge Assistant",
        page_icon=COUCHBASE_LOGO,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": """
            ## Couchbase Book Knowledge Assistant
            ### Powered by Capella AI Services

            This AI Assistant uses RAG (Retrieval-Augmented Generation) to answer questions about books.
            It combines the power of Couchbase's vector search with AI to provide accurate and contextual answers.
            """
        }
    )

    # Custom CSS for Couchbase styling
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {COUCHBASE_COLORS['background']};
        }}
        .chat-message {{
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }}
        .chat-message.user {{
            background-color: #FFFFFF;
            border: 1px solid {COUCHBASE_COLORS['primary']};
        }}
        .chat-message.assistant {{
            background-color: #FFFFFF;
            border: 1px solid {COUCHBASE_COLORS['secondary']};
        }}
        .stTextInput > div > div > input {{
            background-color: white;
        }}
        .cover-glow {{
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow: 0 0 5px {COUCHBASE_COLORS['primary']};
            position: relative;
            z-index: -1;
            border-radius: 3px;
        }}
        .sidebar .sidebar-content {{
            background-color: {COUCHBASE_COLORS['secondary']};
            color: white;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {COUCHBASE_COLORS['primary']};
        }}
        </style>
    """, unsafe_allow_html=True)

    # Sidebar content
    with st.sidebar:
        st.markdown(f"""
            <div style='text-align: center;'>
                <img src='{COUCHBASE_LOGO}' class='cover-glow' style='width: 100px; height: auto;'>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        ## About
        **Couchbase Book Knowledge Assistant**\n
        **Powered by Capella AI Services**\n
        This AI Assistant uses RAG (Retrieval-Augmented Generation) to answer questions about books.
        It combines the power of Couchbase's vector search with AI to provide accurate and contextual answers.
        """)
        
        st.markdown("---")
        st.markdown("""
        ### How to Use
        - Ask questions about books and their content
        - Get contextual answers based on the book's content
        - View relevant images and visualizations
        - Explore book-related information
        """)

    # Main title with Couchbase styling
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: {COUCHBASE_COLORS['primary']};'>Couchbase Book Knowledge Assistant</h1>
        </div>
    """, unsafe_allow_html=True) 