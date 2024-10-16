import streamlit as st
from streamlit_chat import message
import emoji
from llm import get_response

# if 'messages' not in st.session_state:
#     st.session_state['messages'] =[]
    
# st.set_page_config(page_title='Chatbot',page_icon=':robot_face:')
# st.markdown("<h1 style='text-align=center;'>How can I assist you today?</h1>",unsafe_allow_html=True)
# response_container = st.container()
# container = st.container()

# with container:
#     with st.form(key='my_form', clear_on_submit=True):
#         user_input = st.text_area("Your question goes here:", key='input', height=100)
#         submit_button = st.form_submit_button(label='Send')
#         if submit_button:
#             st.session_state['messages'].append(user_input)
#             model_response=get_response(user_input)
#             st.session_state['messages'].append(model_response)
#             with response_container:
#                 for i in range(len(st.session_state['messages'])):
#                         if (i % 2) == 0:
#                             message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
#                         else:
#                             message(st.session_state['messages'][i], key=str(i) + '_AI')


if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = get_response(prompt,st.session_state['messages'])
        st.session_state.messages.append({"role": "assistant", "content": stream})
        response = st.write(st.session_state.messages[-1]['content'])
        print(st.session_state['messages']) 
    