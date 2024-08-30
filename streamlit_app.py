import streamlit as st
import matplotlib.pyplot as plt
import time
import random
import csv
import os

# File to store the leaderboard
LEADERBOARD_FILE = "leaderboard.csv"

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

def load_leaderboard():
    """Loads the leaderboard from the CSV file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            reader = csv.reader(f)
            return [(name, float(score)) for name, score in reader]
    return []

def save_leaderboard(leaderboard):
    """Saves the leaderboard to the CSV file."""
    with open(LEADERBOARD_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(leaderboard)

def add_to_leaderboard(name, score):
    """Adds a new score to the leaderboard, sorts it, and saves to the CSV file."""
    leaderboard = load_leaderboard()
    leaderboard.append((name, score))
    # Sort the leaderboard by score in ascending order and keep the top 10 entries
    leaderboard = sorted(leaderboard, key=lambda x: x[1])[:10]
    save_leaderboard(leaderboard)
    return leaderboard

def display_leaderboard():
    """Displays the leaderboard."""
    leaderboard = load_leaderboard()
    if leaderboard:
        st.write("## Leaderboard")
        for idx, (name, score) in enumerate(leaderboard, start=1):
            st.write(f"{idx}. {name} - {score:.3f} seconds")
    else:
        st.write("No scores yet. Be the first to set a record!")

def start_race():
    st.session_state.colors = ['black'] * 5
    st.session_state.ready_to_click = False
    st.session_state.race_started = True

def record_reaction():
    if st.session_state.ready_to_click:
        end_time = time.time()
        reaction_time = end_time - st.session_state.start_time
        st.session_state.ready_to_click = False
        st.session_state.last_reaction_time = reaction_time
    else:
        st.session_state.false_start = True

def submit_score(name):
    if name:
        st.session_state.leaderboard = add_to_leaderboard(name, st.session_state.last_reaction_time)
        del st.session_state.last_reaction_time
        st.session_state.score_submitted = True
    else:
        st.session_state.name_missing = True

def main():
    st.title("Welcome to F1 Grand Prix!")

    # Initialize session state variables
    if 'colors' not in st.session_state:
        st.session_state.colors = ['black'] * 5
        st.session_state.ready_to_click = False
        st.session_state.race_started = False
        st.session_state.false_start = False
        st.session_state.score_submitted = False
        st.session_state.name_missing = False

    fig = draw_lights(st.session_state.colors)
    fig_placeholder = st.empty()
    fig_placeholder.pyplot(fig)

    if st.button('Start Race', on_click=start_race):
        pass

    if st.session_state.race_started:
        for i in range(5):
            st.session_state.colors[i] = 'red'
            fig = draw_lights(st.session_state.colors)
            fig_placeholder.pyplot(fig)
            time.sleep(random.uniform(0.8, 1.0))
        
        time.sleep(random.uniform(0.8, 1.2))
        st.session_state.colors = ['black'] * 5
        fig = draw_lights(st.session_state.colors)
        fig_placeholder.pyplot(fig)
        st.session_state.start_time = time.time()
        st.session_state.ready_to_click = True
        st.session_state.race_started = False

    if st.button('GO!', on_click=record_reaction):
        pass

    if st.session_state.false_start:
        st.error("False Start! Wait for all lights to turn off.")
        st.session_state.false_start = False

    if 'last_reaction_time' in st.session_state:
        st.write(f"Your reaction time: {st.session_state.last_reaction_time:.3f} seconds")
        name = st.text_input("Enter your name for the leaderboard:", "")
        if st.button("Submit Score", on_click=submit_score, args=(name,)):
            pass

    if st.session_state.score_submitted:
        st.success("Score submitted successfully!")
        st.session_state.score_submitted = False

    if st.session_state.name_missing:
        st.warning("Please enter a name before submitting your score.")
        st.session_state.name_missing = False

    display_leaderboard()

if __name__ == "__main__":
    main()
