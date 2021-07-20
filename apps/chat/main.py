import streamlit as st
from streamlit.server.server import Server
from streamlit.report_thread import get_report_ctx
import datetime
import asyncio

current_session_id = get_report_ctx().session_id


def count_online_users():
    session_infos = Server.get_current()._session_info_by_id.values()
    session_counter = 0
    for session_info in session_infos:
        session_counter += 1
    return session_counter


def rerun_all(current_session_id):
    session_infos = Server.get_current()._session_info_by_id.values()
    for session_info in session_infos:
        session_info.session.flush_browser_queue()
        session_info.session.request_rerun()

st.rerun = rerun_all


@st.cache(allow_output_mutation=True)
def message():
    ts = datetime.datetime.now().timestamp()
    return {"1": {"timestamp": ts, "user": "System", "message": "Welcome"}}


def print_messages(plh_messages):
    messages = message()
    lst = list(messages.items())
    msg_body = ""
    for i in reversed(lst):
        msg_ts = i[1]["timestamp"]
        msg_datetime = datetime.datetime.fromtimestamp(msg_ts)
        msg_user = i[1]["user"]
        msg_text = i[1]["message"]
        msg_body += f"**{msg_user}** ({msg_datetime})\n\n"
        msg_body += f"> {msg_text}\n\n"
    plh_messages.markdown(msg_body)


async def watch(plh_messages):
    while True:
        messages = message()
        if len(messages) != st.session_state.msg_count:
            st.session_state.msg_count = len(messages)
            print_messages(plh_messages)

        _ = await asyncio.sleep(1)


def chat():
    st.write(f"Online users: **{count_online_users()}**")
    username = st.text_input("What's your name?")
    with st.form(key='chat_form', clear_on_submit=True):
        your_message = st.text_input("What's your message?")
        btn_send = st.form_submit_button(label='Send')

    st.subheader("Chat Board")
    st.write("")
    messages = message()
    st.session_state.msg_count = len(messages)
    lst = list(messages.items())

    last_user = lst[-1][1]["user"]
    last_message = lst[-1][1]["message"]
    if (len(username) > 0 and len(your_message) > 0) and (last_user != username or last_message != your_message):
        ts = datetime.datetime.now().timestamp()
        messages[len(messages) + 1] = {"timestamp": ts,
                                       "user": username,
                                       "message": your_message}
        # st.rerun(current_session_id)

    plh_messages = st.empty()
    print_messages(plh_messages)
    asyncio.run(watch(plh_messages))


if __name__ == '__main__':
    chat()
