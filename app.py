import streamlit as st
from moderator import get_most_relevant_user, get_reply, get_all_users

st.title("Cousins.AI")

# Sidebar with users
# st.sidebar.title("Cousins")
users = []
all_users = get_all_users()
for user in all_users:
    users.append(user["name"])
    st.sidebar.write(user["name"])

    

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    interested_user  = get_most_relevant_user(prompt)
    print("interested_user=-----",interested_user)

    chat_reply = get_reply(interested_user, prompt)

    response = f"{interested_user}: {chat_reply}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})