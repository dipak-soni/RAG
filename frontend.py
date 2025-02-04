# import streamlit as st
# from streamlit_chat import message
# import emoji
# from llm import get_response



# if "messages" not in st.session_state:
#     st.session_state.messages = []
    
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])



# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     with st.chat_message("assistant"):
#         stream = get_response(prompt,st.session_state['messages'])
#         st.session_state.messages.append({"role": "assistant", "content": stream})
#         response = st.write(st.session_state.messages[-1]['content'])
#         print(st.session_state['messages']) 



import streamlit as st
import os
from streamlit_chat import message
import emoji
from llm import get_response
from push_to_pinecone import push
from pathlib import Path


# Create 'uploads' directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = None

# File upload section
st.sidebar.header("Upload a File")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "pdf", "png", "jpg", "jpeg"], accept_multiple_files=False)

if uploaded_file and uploaded_file.name != st.session_state['uploaded_file_name']:
        st.session_state['uploaded_file_name'] = uploaded_file.name

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        # #delete all files in a directory 
        # directory = os.path.join(os.getcwd(),'uploads')
        # if os.path.exists(directory):
        #     for file in os.listdir(directory):
        #         print(file)
        #         file_path = os.path.join(directory, file)
        #         print(file_path)
        #         os.remove(file_path)
        #     print(f"All files in '{directory}' have been deleted.")
        # else:
        #     print(f"Directory '{directory}' does not exist.")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # st.sidebar.success(f"File saved: {file_path}")
        
        with st.sidebar.status('Please wait'):
            push(uploaded_file.name)


# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        stream = get_response(prompt, st.session_state['messages'])
        st.session_state.messages.append({"role": "assistant", "content": stream})
        st.write(st.session_state.messages[-1]['content'])
        print(st.session_state['messages'])
