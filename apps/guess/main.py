import streamlit as st
import random


def reset(maximum_number):
    st.session_state.counter = 0
    st.session_state.random_number = random.randint(1, maximum_number)


def guess():
    reset_state = False
    maximum_number = int(st.number_input("What is your maximum number?",
                                         value=1000,
                                         step=1, min_value=10))

    if 'maximum_number' not in st.session_state:
        st.session_state.maximum_number = maximum_number

    if st.session_state.maximum_number != maximum_number:
        reset_state = True
        st.session_state.maximum_number = maximum_number

    if ('random_number' not in st.session_state) or reset_state:
        reset(maximum_number)
        st.info("I have chosen a random number. Guess what my number is!")

    random_number = st.session_state.random_number

    guess_number = st.number_input("What is your guess?",
                                   value=0,
                                   step=1, max_value=maximum_number)
    if guess_number > 0:
        st.session_state.counter += 1

        if guess_number == random_number:
            st.success(f"Congratulation you guessed correctly in {st.session_state.counter} guesses.")
            st.balloons()
            reset(maximum_number)
        elif guess_number < random_number:
            st.info(f"Try {st.session_state.counter} - My number is higher.")
        elif guess_number > random_number:
            st.warning(f"Try {st.session_state.counter} - My number is lower.")


if __name__ == '__main__':
    guess()
