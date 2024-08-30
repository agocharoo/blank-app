import streamlit as st
import matplotlib.pyplot as plt
import time
import random

def draw_lights(colors):
    """Draws F1 starting lights based on the specified colors."""
    fig, ax = plt.subplots(figsize=(6, 1))
    for i, color in enumerate(colors):
        circle = plt.Circle((i + 1, 0.5), 0.4, color=color)
        ax.add_artist(circle)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig

def add_to_leaderboard(name, score):
    """Adds a new score to the leaderboard and sorts it, storing in session state."""
    if 'leaderboard' not in st.session_state or not st.session_state.leaderboard:
        st.session_state.leaderboard = []
    st.session_state.leaderboard.append((name, score))
    # Sort the leaderboard by score in ascending order and keep the top 10 entries
    st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1])[:10]

def display_leaderboard():
    """Displays the leaderboard."""
    if 'leaderboard' in st.session_state and st.session_state.leaderboard:
        st.write("## Leaderboard")
        for idx, (name, score) in enumerate(st.session_state.leaderboard, start=1):
            st.write(f"{idx}. {name} - {score:.3f} seconds")
    else:
        st.write("No scores yet. Be the first to set a record!")

def main():
    st.title("Welcome to F1 Grand Prix!")
    if 'colors' not in st.session_state:
        st.session_state.colors = ['black'] * 5
        st.session_state.ready_to_click = False

    fig = draw_lights(st.session_state.colors)
    fig_placeholder = st.pyplot(fig)

    if st.button('Start Race'):
        st.session_state.colors = ['black'] * 5
        st.session_state.ready_to_click = False
        fig = draw_lights(st.session_state.colors)
        fig_placeholder.pyplot(fig)
        for i in range(5):
            delay = random.uniform(0.8, 1.0)
            time.sleep(delay)
            st.session_state.colors[i] = 'red'
            fig = draw_lights(st.session_state.colors)
            fig_placeholder.pyplot(fig)
        time.sleep(random.uniform(0.8, 1.2))
        st.session_state.colors = ['black'] * 5
        fig = draw_lights(st.session_state.colors)
        fig_placeholder.pyplot(fig)
        st.session_state.start_time = time.time()
        st.session_state.ready_to_click = True

    if st.button('GO!'):
        if st.session_state.ready_to_click:
            end_time = time.time()
            reaction_time = end_time - st.session_state.start_time
            st.session_state.ready_to_click = False
            name = st.text_input("Congratulations! Enter your name for the leaderboard:", "")
            if name:  # Ensure name is entered before updating the leaderboard
                add_to_leaderboard(name, reaction_time)
        else:
            st.error("False Start! Wait for all lights to turn off.")

    display_leaderboard()  # Display the leaderboard regardless of other actions

if __name__ == "__main__":
    main()
