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
    """Adds a new score to the leaderboard and sorts it."""
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = []
    st.session_state.leaderboard.append((name, score))
    st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1])[:10]

def display_leaderboard():
    """Displays the top 10 scores from the leaderboard."""
    if 'leaderboard' in st.session_state and st.session_state.leaderboard:
        st.write("## Leaderboard")
        for idx, (name, score) in enumerate(st.session_state.leaderboard, start=1):
            st.write(f"{idx}. {name} - {score:.3f} seconds")
    else:
        st.write("No scores yet. Be the first to set a record!")

def main():
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
    image_path = 'checkerd_flag.jpg'
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
        for i in range(5):
            delay = random.uniform(0.8, 1.0)
            time.sleep(delay)
            st.session_state['colors'][i] = 'red'
            fig = draw_lights(st.session_state['colors'])
            fig_placeholder.pyplot(fig)
        time.sleep(random.uniform(0.8, 1.2))
        st.session_state['colors'] = ['black'] * 5
        fig = draw_lights(st.session_state['colors'])
        fig_placeholder.pyplot(fig)
        st.session_state['start_time'] = time.time()
        st.session_state['ready_to_click'] = True

    st.markdown("**Instructions:** Once all lights turn off, hit the **GO!** button as soon as possible.")

    if st.button('GO!'):
        if st.session_state['ready_to_click']:
            end_time = time.time()
            reaction_time = end_time - st.session_state['start_time']
            st.session_state['ready_to_click'] = False
            name = st.text_input("Congratulations! Enter your name for the leaderboard:", "")
            if name:
                add_to_leaderboard(name, reaction_time)
            display_leaderboard()
        else:
            st.error("False Start!")
            st.write("Time for a pit stop with the stewards!")

    footer = """
    <div class='footer'>
        <p>Created by <a href='https://www.linkedin.com/in/mohit-choudhary-87832882/' target='_blank'>Mohit Choudhary</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
