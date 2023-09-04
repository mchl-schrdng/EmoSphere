vimport streamlit as st
from utils.database import insert_word

# Display centered logo
st.write("<div style='text-align: center;'><br>", unsafe_allow_html=True)
st.image("images/logo.png", width=200)
st.write("</div>", unsafe_allow_html=True)

# Main function for Streamlit app
def main():
    st.title("EmoSphere: A Real-Time Collective Emotional Landscape")

    # Word Submission
    user_input = st.text_input("Enter a word that encapsulates your current emotional state:")

    if user_input:
        insert_word(user_input)

    # Time Slider
    time_range = st.slider("Select time range:", 0, 24, (0, 24))

    # TODO: Retrieve words from the database based on the selected time range

    # TODO: Generate and display the word cloud

if __name__ == "__main__":
    main()
