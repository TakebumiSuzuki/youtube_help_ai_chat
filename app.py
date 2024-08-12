import ui_constants as UC
import conversation_logic as logic
import streamlit as st
import uuid
import time # Gemini使用でストリームする場合のみ使う
import random # Gemini使用でストリームする場合のみ使う

MAX_USER_INPUT = 200

ss = st.session_state

if "conversation" not in ss:
    ss["conversation"] = []
message_list = ss["conversation"]

if "docs_store" not in ss:
    ss["docs_store"] = {}

if "current_docs" not in ss:
    ss["current_docs"] = ""

if "show_clear_button" not in ss:
    ss["show_clear_button"] = False

if "language" not in ss:
    ss["language"] = 'Japanese'

st.set_page_config(
     page_title = UC.TAB_TITLE(ss["language"]),
     layout = "wide",
     initial_sidebar_state = "expanded"
)

# unsafe_allow_html=True を使用して、HTMLとCSSの直接挿入を許可
st.markdown(UC.CSS, unsafe_allow_html=True)

st.title(UC.TITLE(ss["language"]))
st.write(UC.SUBTITLE(ss["language"]))

# Display chat messages from history on app rerun
if message_list != []:
    for message in message_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "AI":
                if st.button('docs履歴', key = message["key"]):
                    ss["current_docs"] = ss["docs_store"][message["key"]]

    if ss["show_clear_button"] == True:
        clear_button = st.button(UC.CLEAR_BUTTON(ss["language"]))
        if clear_button == True:
            ss["conversation"] = []
            ss["current_docs"] = ""
            clear_button = False
            st.rerun()

def hide_clear_button():
    ss["show_clear_button"] = False

# Accept user input
if input := st.chat_input(UC.INPUT_HOLDER(ss["language"]), on_submit = hide_clear_button):
    # インプとの文字数のモデレート
    if len(input) > MAX_USER_INPUT:
        input = input[:MAX_USER_INPUT]
    #ユーザーからのインプットをそのままUIに表示する
    with st.chat_message("user"):
        st.markdown(input)
    #ユーザーからのインプットをsession_stateに記録
    ss["conversation"].append({"role" : "user", "content" : input})

    #AIからの返答をストリームにて取得、表示する
    with st.chat_message("AI"):
        msg_holder = st.empty()
        msg_holder.markdown("Searching...")

        sources, language = logic.handle_retrieval(input)
        ss["current_docs"] = sources
        ss["language"] = language
        print(ss['language'])

        with st.sidebar:
            st.subheader(UC.SIDEBAR_SUBTITLE(ss["language"]))

            if "current_docs" in ss:
                st.markdown(ss["current_docs"])

        msg_holder.markdown("Reading source documents...")
        full_response = ""
        stream = logic.get_stream(input, sources, ss['language'])
        for chunk in stream:
            try:
                # Geminiの場合
                # word_count = 0
                # random_int = random.randint(5, 10)
                # for word in chunk.text:
                #     full_response += word
                #     word_count += 1
                #     if word_count == random_int:
                #         msg_holder.markdown(full_response + "_")
                #         time.sleep(0.02)
                #         word_count = 0
                #         random_int = random.randint(5, 10)

                #OpenAIの場合
                if chunk.choices[0].delta.content is None: # ストリームの最後で必ず一回Noneが送られるようなのでその処理
                    continue
                for word in chunk.choices[0].delta.content:
                    full_response += word
                    msg_holder.markdown(full_response + "_")
                    # time sleepは、1chunkあたり1から数文字程度なのでopenaiの場合必要ない

            except Exception as e:
                print('AIからの回答を記述中に不明のエラーが発生しました: f{e}')
                raise

        msg_holder.markdown(full_response)


    #AIからの返答をsession_stateに記録
    generated_key = uuid.uuid4()
    ss["conversation"].append({"role" : "AI", "content" : full_response, "key" : generated_key})
    ss["docs_store"][generated_key] = sources
    ss["show_clear_button"] = True
    st.rerun()

else:
    with st.sidebar:
        st.subheader(UC.SIDEBAR_SUBTITLE(ss["language"]))
        if "current_docs" in ss:
            st.markdown(ss["current_docs"])






