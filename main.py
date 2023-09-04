from utils.database import insert_word, retrieve_words
from wordcloud import WordCloud
import streamlit as st
import base64
import matplotlib.pyplot as plt

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

    # Time Slider
    time_range = st.slider("Select time range:", 0, 24, (0, 24))

    # Retrieve words from the database based on the selected time range
    words_data = retrieve_words(time_range)

    # Generate and display the word cloud
    if words_data:
        words = [item['word'] for item in words_data.data]  # Updated line
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))

        # Display Word Cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.image(plt, caption="Emotional Landscape", use_column_width=True)

if __name__ == "__main__":
    main()
