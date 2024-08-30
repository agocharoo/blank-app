import streamlit as st
import matplotlib.pyplot as plt
import time
import random
import csv
import os

# File to store the scores
SCORE_FILE = "score.csv"

def draw_lights(colors):
    """Draws the lights with specified colors, ensuring they appear circular and with reduced padding."""
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
    """Loads the leaderboard from the CSV file with error handling."""
    leaderboard = []
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 2:
                        name, score = row
                        try:
                            score = float(score)
                            leaderboard.append((name, score))
                        except ValueError:
                            st.warning(f"Invalid score format for {name}: {score}")
                    else:
                        st.warning(f"Invalid row in CSV: {row}")
        except Exception as e:
            st.error(f"Error reading the leaderboard file: {e}")
    return leaderboard

def save_leaderboard(leaderboard):
    """Saves the leaderboard to the CSV file with error handling."""
    try:
        with open(SCORE_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(leaderboard)
    except Exception as e:
        st.error(f"Error saving the leaderboard: {e}")

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

def main():
    # Custom CSS to center the title and tweak other styling
    st.markdown("""
    <style>
    .reportview-container .markdown-text-container {
        text-align: center;
    }
    .reportview-container .fullScreenFrame > div {
        display: flex;
        justify-content: center;
    }
    h1 {
        text-align: center;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
    }
    a:link, a:visited {
        color: blue;
        background-color: transparent;
        text-decoration: none;
    }
    a:hover, a:active {
        color: red;
        background-color: transparent;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Welcome to F1 Grand Prix!")

    # Image at the top of the app
    image_path = 'checkerd_flag.jpg'  # Adjust path as needed
    st.image(image_path, use_column_width=True)

    if 'colors' not in st.session_state:
        st.session_state['colors'] = ['black'] * 5
        st.session_state['ready_to_click'] = False
    
    fig = draw_lights(st.session_state['colors'])
    fig_placeholder = st.pyplot(fig)

    if st.button('Start Race'):
        st.session_state['colors'] = ['black'] * 5
        st.session_state['ready_to_click'] = False
        fig = draw_lights(st.session_state['colors'])
        fig_placeholder.pyplot(fig)
        # Lights turn red sequentially
        for i in range(5):
            delay = random.uniform(0.8, 1.0)  # Simulating random delay
            time.sleep(delay)
            st.session_state['colors'][i] = 'red'
            fig = draw_lights(st.session_state['colors'])
            fig_placeholder.pyplot(fig)
        # Lights turn off simultaneously
        time.sleep(random.uniform(0.8, 1.2))
        st.session_state['colors'] = ['black'] * 5
        fig = draw_lights(st.session_state['colors'])
        fig_placeholder.pyplot(fig)
        st.session_state['start_time'] = time.time()
        st.session_state['ready_to_click'] = True

    st.markdown("""
    **Instructions:**
    - Once all lights turn off, hit the **GO!** button as soon as possible to simulate your reaction.
    """)

    if st.button('GO!'):
        if 'ready_to_click' in st.session_state and st.session_state['ready_to_click']:
            end_time = time.time()
            reaction_time = end_time - st.session_state['start_time']
            st.write(f"Your reaction time is {reaction_time:.3f} seconds.")
            st.session_state['last_reaction_time'] = reaction_time
            st.session_state['ready_to_click'] = False
        else:
            st.error("False Start!")
            st.write("Time for a pit stop with the stewards!")

    # Add name input and submit score button if there's a reaction time to submit
    if 'last_reaction_time' in st.session_state:
        name = st.text_input("Enter your name for the leaderboard:", "")
        if st.button("Submit Score"):
            if name:
                add_to_leaderboard(name, st.session_state['last_reaction_time'])
                st.success("Score submitted successfully!")
                del st.session_state['last_reaction_time']
            else:
                st.warning("Please enter a name before submitting your score.")

    # Display the leaderboard
    display_leaderboard()

    # Footer
    footer = """
    <div class='footer'>
        <p>Created by <a href='https://www.linkedin.com/in/mohit-choudhary-87832882/' target='_blank'>Mohit Choudhary</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
