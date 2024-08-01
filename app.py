import constants as K
import streamlit as st
import conversation_logic as logic
import time
import random
import uuid

st.set_page_config(
     page_title = K.TAB_TITLE(K.lang),
     layout = "wide",
     initial_sidebar_state = "expanded"
)

ss = st.session_state

if "conversation" not in ss:
    ss["conversation"] = []
message_list = ss["conversation"]

if "docs_store" not in ss:
    ss["docs_store"] = {}

if "current_text" not in ss:
    ss["current_text"] = ""

# unsafe_allow_html=True を使用して、HTMLとCSSの直接挿入を許可
st.markdown(K.CSS, unsafe_allow_html=True)

st.title(K.TITLE(K.lang))
st.write(K.SUBTITLE(K.lang))

# Display chat messages from history on app rerun
if message_list != []:
    for message in message_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "AI":
                if st.button('docs履歴', key = message["key"]):
                    ss["current_text"] = ss["docs_store"][message["key"]]

    if "show_clear" in ss and ss["show_clear"] == True:
        clear_button = st.button(K.CLEAR_BUTTON(K.lang))
        if clear_button == True:
            ss["conversation"] = []
            ss["current_text"] = ""
            clear_button = False
            st.rerun()

def hide_clear():
    ss["show_clear"] = False

# Accept user input
if input := st.chat_input(K.INPUT_HOLDER(K.lang), on_submit = hide_clear):

    #ユーザーからのインプットをそのままUIに表示する
    with st.chat_message("user"):
        st.markdown(input)
    #ユーザーからのインプットをsession_stateに記録
    ss["conversation"].append({"role" : "user", "content" : input})

    #AIからの返答をストリームにて取得、表示する
    with st.chat_message("AI"):
        msg_holder = st.empty()
        msg_holder.markdown("Searching...")
        text = logic.retrieve_text(input)
        ss["current_text"] = text

        with st.sidebar:
            st.subheader(K.SIDEBAR_SUBTITLE(K.lang))

            if "current_text" in ss:
                st.markdown(ss["current_text"])

        msg_holder.markdown("Reading source documents...")
        full_response = ""
        stream = logic.get_stream(input, text)
        for chunk in stream:
            try:
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        msg_holder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            except Exception as e:
                logic.error_handling(e)

        msg_holder.markdown(full_response)


    #AIからの返答をsession_stateに記録
    generated_key = uuid.uuid4()
    ss["conversation"].append({"role" : "AI", "content" : full_response, "key" : generated_key})
    ss["docs_store"][generated_key] = text
    ss["show_clear"] = True
    st.rerun()


else:
    with st.sidebar:
        st.subheader(K.SIDEBAR_SUBTITLE(K.lang))
        if "current_text" in ss:
            st.markdown(ss["current_text"])




