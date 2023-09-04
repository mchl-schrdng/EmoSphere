import streamlit as st
import base64
from utils.database import insert_word

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
img_base64 = get_image_base64("assets/images/logo.png")

# Display centered logo
st.markdown(f'<p class="centered"><img src="data:image/png;base64,{img_base64}" style="max-width:200px; height:auto;"></p>', unsafe_allow_html=True)

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
