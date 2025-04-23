import streamlit as st
import asyncio
from main import CouchbaseRAG
import json
from typing import List, Dict
import base64
from langchain_core.messages import AIMessage, HumanMessage
from app_ui import init_ui, COUCHBASE_LOGO
import re

# Initialize UI
init_ui()

def format_markdown(text: str) -> str:
    """Format the response text using proper Markdown formatting with better structure"""
    # Remove any internal thinking markers
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Split into paragraphs
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    
    # Check if the text contains structured information
    if any(line.startswith('-') for line in text.split('\n')):
        # Format as a structured response
        formatted_paragraphs.append("## Answer")
        formatted_paragraphs.append("")
        
        current_section = None
        for para in paragraphs:
            # Skip empty paragraphs
            if not para.strip():
                continue
                
            # Format section headers
            if para.strip().startswith('-'):
                if current_section:
                    formatted_paragraphs.append("")
                current_section = para.strip('- ').strip()
                formatted_paragraphs.append(f"### {current_section}")
                continue
                
            # Format content under sections
            if current_section:
                formatted_paragraphs.append(para)
            else:
                formatted_paragraphs.append(para)
    else:
        # Format as a regular response
        for para in paragraphs:
            if not para.strip():
                continue
                
            # Format headings
            if para.startswith('#'):
                formatted_paragraphs.append(para)
                continue
                
            # Format lists
            if para.strip().startswith('-') or para.strip().startswith('*'):
                lines = para.split('\n')
                formatted_lines = []
                for line in lines:
                    if line.strip().startswith(('-', '*')):
                        formatted_lines.append(line)
                    else:
                        formatted_lines[-1] += ' ' + line.strip()
                formatted_paragraphs.append('\n'.join(formatted_lines))
                continue
                
            # Format code blocks
            if '```' in para:
                formatted_paragraphs.append(para)
                continue
                
            # Regular paragraphs
            formatted_paragraphs.append(para)
    
    # Join paragraphs with proper spacing
    return '\n\n'.join(formatted_paragraphs)

def convert_to_langchain_messages(messages: List[Dict]) -> List[Dict]:
    """Convert message format to be compatible with LangChain"""
    langchain_messages = []
    for msg in messages:
        if isinstance(msg, dict):
            if msg["role"] == "user":
                langchain_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                langchain_messages.append({"role": "assistant", "content": msg["content"]})
        elif isinstance(msg, (AIMessage, HumanMessage)):
            langchain_messages.append({"role": "assistant" if isinstance(msg, AIMessage) else "user", "content": msg.content})
    return langchain_messages

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your Couchbase Book Knowledge Assistant. How can I help you today?"}]

# Initialize RAG system
@st.cache_resource
def get_rag_system():
    return CouchbaseRAG()

# Display chat messages with improved styling
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=COUCHBASE_LOGO if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if "image_url" in msg and msg["image_url"]:
            st.image(msg["image_url"], width=300)

# Chat input with improved styling
if prompt := st.chat_input("Ask a question about books..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Get RAG system response
    with st.chat_message("assistant", avatar=COUCHBASE_LOGO):
        with st.spinner("Thinking..."):
            try:
                rag = get_rag_system()
                # Convert messages to LangChain format
                langchain_messages = convert_to_langchain_messages(st.session_state.messages)
                response = asyncio.run(rag.generate_rag_response(
                    langchain_messages,
                    prompt
                ))
                
                # Display text response with streaming
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response["text_stream"]:
                    token = chunk.choices[0].delta.content
                    if token:
                        full_response += token
                        formatted_response = format_markdown(full_response)
                        message_placeholder.markdown(formatted_response + "▌")
                
                # Final formatting of the complete response
                formatted_response = format_markdown(full_response)
                message_placeholder.markdown(formatted_response)
                
                # Display image if available
                if response["image_url"]:
                    st.image(response["image_url"], width=300)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": formatted_response,
                    "image_url": response["image_url"]
                })
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Sorry, I encountered an error: {str(e)}"
                }) 