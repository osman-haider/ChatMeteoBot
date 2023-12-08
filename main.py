import streamlit as st
from chatbot import RuleBot
import locationtagger


st.set_page_config(page_title="ChatMeteoBot")
AlienBot = RuleBot()
st.title("ChatMeteoBot")

bot_replay = None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# React to user input
if prompt := st.chat_input("write your message"):
    place_entity = locationtagger.find_locations(text=prompt)
    if place_entity.cities:
        bot_replay = AlienBot.chat(prompt)
    else:
        lower_prompt = prompt.lower()
        bot_replay = AlienBot.chat(lower_prompt)

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    stringvar = ""
    if isinstance(bot_replay,dict):
        for key, value in bot_replay.items():
            stringvar += f"{key} : {value}\n\n"
        with st.chat_message("assistant"):
            st.markdown(stringvar)
        st.session_state.messages.append({"role": "assistant", "content": stringvar})

    else:
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(bot_replay)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_replay})
