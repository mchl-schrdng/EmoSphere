import streamlit as st
import base64
import matplotlib.pyplot as plt
from datetime import date
from wordcloud import WordCloud
from collections import Counter
from utils.database import insert_word, retrieve_words, get_word_frequencies

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Style
st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Get the Base64 string of the image
img_base64 = get_image_base64("images/logo.png")

# Display centered logo
st.markdown(f'<p class="centered"><img src="data:image/png;base64,{img_base64}" style="max-width:200px; height:auto;"></p>', unsafe_allow_html=True)

# Display centered title
st.markdown('<h1 class="centered">EmoSphere</h1>', unsafe_allow_html=True)

# Main function for Streamlit app
def main():
    # Word Submission
    user_input = st.text_input("Enter a word that encapsulates your current emotional state:")

    if user_input:
        insert_word(user_input)

    # Date Slider
    start_date = date(2023, 9, 1)
    end_date = date.today()
    time_range = st.date_input("Select date range:", [start_date, end_date])

    # Retrieve word frequencies from the database based on the selected time range
    word_frequencies = get_word_frequencies(time_range)

    # Generate and display the word cloud
    if word_frequencies:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies)

        # Display Word Cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)  # Streamlit's way to display matplotlib plots

    # Clear database
    if st.button("Clear Database"):
        clear_database()

    # Export word frequencies
    if st.button("Export Word Frequencies"):
        export_word_frequencies()

    # Filter word frequencies by emotion
    emotion = st.selectbox("Filter by emotion:", ["Happy", "Sad", "Angry", "Fearful", "Surprised", "Disgusted"])
    if emotion:
        filtered_word_frequencies = filter_word_frequencies(word_frequencies, emotion)
        if filtered_word_frequencies:
            st.markdown(f"Word frequencies for {emotion}:")
            st.table(filtered_word_frequencies.most_common())

if __name__ == "__main__":
    main()