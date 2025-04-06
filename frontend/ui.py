import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY_PLACEHOLDER = "< ----- ADD YOUR API KEY HERE ------ >"
API_KEY = os.getenv("API_KEY", API_KEY_PLACEHOLDER)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8001")

def getHeader(header):
    """
    Resuable header code

    Args:
        header(str) -> header string to be populated in header
    """
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>C-One Chatbot</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center;'>{header}</h4>", unsafe_allow_html=True)


def show_fallback_ui():
    """Display fallback UI when API key is missing."""
    st.title("Missing API Key")
    st.error("Your `.env` file contains an invalid API key placeholder.")
    st.write("Please update your `.env` file with a valid API key and restart the application.")


def create_simple_chat_app():
    """
    Simple chat app for Streamlit UI
    """

    # Sidebar configuration
    st.sidebar.title("Menu")
    section = st.sidebar.radio(
        "Choose a section:",
        ("Chat", "RAG Ingestion Web", "RAG Ingestion PDF")
    )
    

    logo_path = "../public/cdw.png" 
    col1, col2, col3 = st.columns([2, 1, 2]) 
    with col2:
        st.image(logo_path, width=150)

    # Condition for poem generation page
    if section == "Chat":  
        getHeader("Start editing the files and start building project, to test the whether the <span style='color: #FF4B4B'>model</span> works try <span style='color: #FF4B4B'>chatting</span> by adding the api key in <i style='color: #FF4B4B'>.env</i>")

        # Maintain chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User Input Box
        user_input = st.chat_input("Type your message...")

        if user_input:
            # Display user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Generate bot response from server
            try:
                server_response = requests.post(f"{BACKEND_URL}/invoke", json={"user_query": user_input})
                content = "Failed to get a response from the AI."
                if server_response.status_code == 200:
                    json_data = server_response.json()
            
                    # Check if 'response' key exists in the JSON response
                    if "response" in json_data:
                        content = json_data["response"]
                    else:
                        content = "Response received but in an unexpected format."
                else:
                    content = f"Server error: {server_response.status_code}, Probably due to missing api-key or server code issue."
            except Exception as e:
                content = f"Exception occurred while calling the server {e}"
            
            # Store the bot response in session state
            st.session_state.messages.append({"role": "assistant", "content": content})

            # Display bot response
            with st.chat_message("assistant"):
                st.markdown(content)
    elif section == "RAG Ingestion Web":
        getHeader("RAG Web URL Ingestion")

        url = st.text_input("Enter the document URL:")
        if st.button("Ingest URL"):
            if url:
                response = requests.post(f"{BACKEND_URL}/ingest/url", json={"url": url})

                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(f"Error: {response.json()['detail']}")
            else:
                st.warning("Please enter a URL.")


    elif section =="RAG Ingestion PDF":
        getHeader("RAG File Ingestion")

        uploaded_file = st.file_uploader("Upload a file:", type=["pdf"])

        if uploaded_file is not None:
            # Convert the uploaded file into a format requests can handle
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{BACKEND_URL}/ingest/pdf", files=files)
            
            if response.status_code == 200:
                st.success(f"File '{uploaded_file.name}' uploaded  and file embedding stored in vectordb successfully!") 
            else:
                st.error(f"Failed to upload: {response.json()['detail']}")





if __name__ == "__main__":
    if API_KEY == API_KEY_PLACEHOLDER:
        show_fallback_ui()
    else:
        create_simple_chat_app()



# Run the chatbot with: `streamlit run ui.py`