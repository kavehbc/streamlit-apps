import streamlit as st
import numpy as np
import pandas as pd
import asyncio


def checkRows(board, window=3):
    hr_slider = np.lib.stride_tricks.sliding_window_view(board, window_shape=(1, window))
    for item in hr_slider:
        for row in item:
            row = np.unique(row)
            if len(set(row)) == 1:
                if row[0] != ".":
                    return row[0]
    return None


def checkDiagonals(board, window=3):
    diags = [board[::-1, :].diagonal(i) for i in range(-1 * (len(board) - 1), len(board))]
    diags.extend(board.diagonal(i) for i in range(len(board) - 1, -1 * len(board), -1))

    all_diags = []
    for n in diags:
        if len(n) >= window:
            diag = n.tolist()
            if len(diag) < len(board):
                diff = len(board) - len(diag)
                empty_array = ["."]
                empty_array *= diff
                diag.extend(empty_array)
            all_diags.append(diag)

    df_diagnal = pd.DataFrame(all_diags)
    result = checkRows(df_diagnal)
    if result:
        return result
    return None


def checkWin(board):
    # transposition to check rows, then columns
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)


@st.cache_resource()
def board():
    return np.full((5, 5), ".", dtype=str)


@st.cache_resource()
def select_next_player():
    return ["X"]


async def watch():
    while True:
        game_board = board()
        if "online_board" not in st.session_state:
            local_game_board = np.copy(game_board)
        else:
            local_game_board = st.session_state.online_board
        if not np.array_equal(game_board, local_game_board):
            # st.write("There is an update")
            st.experimental_rerun()
        _ = await asyncio.sleep(1)


def plot_game_board(game_board, i_am):
    # Show one button for each field.
    st.session_state.online_board = np.copy(game_board)
    for i, row in enumerate(game_board):
        cols = st.columns([0.1, 0.1, 0.1, 0.1, 0.1, 0.5])
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"ttt_online_{i}-{j}",
                on_click=handle_click,
                args=(i, j, i_am),
            )
    winner = checkWin(game_board)
    if winner != ".":
        st.session_state.winner = winner
        btn_reset = st.button("Reset")
        if btn_reset:
            reset_game()


def reset_game():
    st.session_state.winner = "."
    # clear cache
    st.cache_data.clear()
    st.cache_resource.clear()

    st.experimental_rerun()


def handle_click(i, j, i_am):
    game_board = board()
    next_player = select_next_player()

    if not st.session_state.winner:
        if i_am == next_player[0]:
            if game_board[i, j] == ".":
                game_board[i, j] = next_player[0]
                next_player[0] = ("O" if next_player[0] == "X" else "X")
            else:
                st.warning("Select an empty box")
        else:
            st.warning("It is not your turn")


def tictactoe_online():
    st.write("")
    st.write("""
        In this game, two players can play together from different devices.
        It is possible for the other users to join and watch the players' game.
    """)
    i_am = st.radio("Who are you?", options=["X", "O"])

    # Initialize state.
    game_board = board()
    next_player = select_next_player()

    if "winner" not in st.session_state:
        st.session_state.winner = None

    st.info(f"**{next_player[0]}** turn")

    plot_game_board(game_board, i_am)

    if st.session_state.winner:
        st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")

    asyncio.run(watch())


if __name__ == '__main__':
    tictactoe_online()
