import streamlit as st
import random

st.title("!!!!GUESS THE GAME!!!!!")
if "number" not in st.session_state:
    st.session_state.number=random.randint(1,100)
    if "attempts" not in st.session_state:
        st.session_state.attempts=0
    max_attempts=5
    guess=st.number_input("Enter the guess (1-100)",min_value =1,max_value=100)
    if st.button("submit guess"):
        st.session_state.attempts+=1
        if guess<st.session_state.number:
            st.write("guess higher ")
        elif guess>st.session_state.number:
            st.write("guess lower")
        else:
            st.write(f"congratulations! you've guessed the number {st.session_state.number}. in {st.session_state.attempts} attempts.")
            st.balloons()
        if st.session_state.attempts>=max_attempts and guess !=st.session_state.number:
            st.error(f"game over! you have used all {max_attempts} attempts. the number was {st.session_state.number}")
            st.write(f"attempts remaining: {max_attempts - st.session_state.attempts}")
            if st.button("Restart"):
                st.session_state.number=random.randint(1,100)
                st.session_state.attempts=0