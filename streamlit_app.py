import streamlit as st
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
import os

def draw_lights(colors):
    fig, ax = plt.subplots(figsize=(6, 1))
    for i, color in enumerate(colors):
        circle = plt.Circle((i + 1, 0.5), 0.4, color=color)
        ax.add_artist(circle)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig

def read_scores():
    if os.path.exists('score.csv'):
        return pd.read_csv('score.csv')
    else:
        return pd.DataFrame(columns=['Name', 'Score'])

def update_leaderboard(new_score, name='XYZ'):
    df = read_scores()
    df = df.append({'Name': name, 'Score': new_score}, ignore_index=True)
    df = df.sort_values('Score').reset_index(drop=True)
    df = df.head(10)  # Keep only the top 10 scores
    df.to_csv('score.csv', index=False)

def get_rank(new_score):
    df = read_scores()
    df = df.append({'Name': 'current_user', 'Score': new_score}, ignore_index=True)
    df = df.sort_values('Score').reset_index(drop=True)
    return df[df['Name'] == 'current_user'].index[0] + 1, df.shape[0]

def main():
    st.markdown("""
    <style>
    ... (existing styles) ...
    </style>
    """, unsafe_allow_html=True)
    st.title("Welcome to F1 Grand Prix!")
    image_path = 'checkerd_flag.jpg'
    st.image(image_path, use_column_width=True)

    if 'colors' not in st.session_state:
        st.session_state['colors'] = ['black'] * 5
        st.session_state['ready_to_click'] = False

    fig = draw_lights(st.session_state['colors'])
    fig_placeholder = st.pyplot(fig, clear_figure=True)

    if st.button('Start Race'):
        ... (existing race logic) ...

    st.markdown("**Instructions:** Once all lights turn off, hit the **GO!** button as soon as possible.")

    if st.button('GO!'):
        if 'ready_to_click' in st.session_state and st.session_state['ready_to_click']:
            end_time = time.time()
            reaction_time = end_time - st.session_state['start_time']
            rank, total_users = get_rank(reaction_time)
            if rank <= 10:
                name = st.text_input("Congratulations! Enter your name for the leaderboard:", "")
                if name:
                    update_leaderboard(reaction_time, name)
                    st.write(f"Your reaction time is {reaction_time:.3f} seconds. Your rank is {rank}!")
            else:
                update_leaderboard(reaction_time)
                st.write(f"Your reaction time is {reaction_time:.3f} seconds. Your rank is {rank} out of {total_users} users.")
            st.table(read_scores()[['Name', 'Score']])
        else:
            st.error("False Start!")
            st.write("Time for a pit stop with the stewards!")

    # Footer
    footer = """
    <div class='footer'>
        <p>Created by <a href='https://www.linkedin.com/in/mohit-choudhary-87832882/' target='_blank'>Mohit Choudhary</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
