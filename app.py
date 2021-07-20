import streamlit as st
from apps.about import about
from apps.guess.main import guess
from apps.tictactoe.main import tictactoe
from apps.tictactoe_online.main import tictactoe_online
from apps.chat.main import chat
from apps.whiteboard.main import whiteboard


# st.set_page_config(page_title="Streamlit Fun Apps")

games_list = {"about": "Home",
              "guess": "Guessing Game",
              "tictactoe": "Tick-Tac-Toe (Offline)",
              "tictactoe_online": "Tick-Tac-Toe (Online)",
              "chat": "Message Board",
              "whiteboard": "Whiteboard (Online)"}


def getAppCode(AppID):
    global games_list
    return games_list.get(AppID)


def main():
    st.title("Streamlit Fun Apps")
    selected_app = st.sidebar.selectbox("Select App",
                                        options=list(games_list.keys()),
                                        format_func=lambda x: getAppCode(x))
    st.header(getAppCode(selected_app))
    eval(selected_app + "()")


if __name__ == '__main__':
    main()
