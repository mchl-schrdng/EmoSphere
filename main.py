import streamlit as st
import base64
import plotly.express as px
import pandas as pd
from datetime import datetime
from utils.database import insert_word, retrieve_words
from utils.sentiment_analysis import get_sentiment

# Load the custom CSS for the background animation
def load_css(filename):
    with open(filename) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('utils/styles.css')


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

img_base64 = get_image_base64("images/logo.png")
st.markdown(f'<p class="centered"><img src="data:image/png;base64,{img_base64}" style="max-width:200px; height:auto;"></p>', unsafe_allow_html=True)
st.markdown('<h1 class="centered">EmoSphere</h1>', unsafe_allow_html=True)

def main():
    st.subheader('', divider='rainbow')
    st.markdown("""
    Welcome to **EmoSphere**, an app that allows you to explore the emotional landscape based on words submitted by users.
    
    ### How to Use
    1. **Enter a Word**: Type a word that represents your current emotion and hit Enter.
    2. **Select Month and Year**: Use the dropdowns to filter the data by a specific month and year.
    3. **View the Graphs**: The bar chart below will update to show the frequency of each word for the selected time period, and the pie chart will show the sentiment distribution of the entered words.
    4. **Sentiment Distribution by Month**: The bar chart below will show the sentiment distribution for each month.
    """)
    st.subheader('', divider='rainbow')
    
    if 'entered_word' not in st.session_state:
        st.session_state.entered_word = ""
    
    st.session_state.entered_word = st.text_input("Enter a word (one word only):", value=st.session_state.entered_word, max_chars=20).lower()
    
    if st.session_state.entered_word:
        if " " in st.session_state.entered_word:
            st.error("Please enter only one word without spaces.")
        else:
            insert_word(st.session_state.entered_word)
            st.session_state.entered_word = ""
    
    raw_data = retrieve_words()
    df_pd = pd.DataFrame(raw_data)
    df_pd['created_at'] = pd.to_datetime(df_pd['created_at'])
    
    st.subheader('', divider='rainbow')
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
    selected_year = st.selectbox("Select Year:", list(range(2020, datetime.now().year + 1)), index=datetime.now().year - 2020)
    
    st.subheader('', divider='rainbow')
    month_number = months.index(selected_month) + 1
    mask = (df_pd['created_at'].dt.month == month_number) & (df_pd['created_at'].dt.year == selected_year)
    filtered_df_pd = df_pd[mask]
    
    word_frequencies = filtered_df_pd['word'].value_counts().reset_index()
    word_frequencies.columns = ['word', 'count']
    
    fig = px.bar(
        word_frequencies.head(5),
        x='word',
        y='count',
        title=f'Top 5 Word Frequencies for {selected_month} {selected_year}',
        color='count',
        color_continuous_scale='rainbow',
    )
    fig.update_traces(marker_line_width=1.5, opacity=0.7)
    fig.update_layout(height=300)  # Adjust the height of the figure
    st.plotly_chart(fig)
    
    sentiment_counts = filtered_df_pd['word'].apply(get_sentiment).value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    
    sentiment_fig = px.pie(
        sentiment_counts,
        names='sentiment',
        values='count',
        title=f'Sentiment Distribution for {selected_month} {selected_year}',
        color_discrete_sequence=['green', 'red', 'gray']
    )
    sentiment_fig.update_layout(height=300)  # Adjust the height of the figure
    st.plotly_chart(sentiment_fig)

    # Sentiment distribution by month
    sentiment_by_month = []
    for month_name in months:
        month_number = months.index(month_name) + 1
        month_mask = (df_pd['created_at'].dt.month == month_number)
        month_sentiments = df_pd[month_mask]['word'].apply(get_sentiment).value_counts().to_dict()
        sentiment_by_month.append({'month': month_name, **month_sentiments})

    sentiment_by_month_df = pd.DataFrame(sentiment_by_month)
    sentiment_by_month_fig = px.bar(
        sentiment_by_month_df.melt(id_vars='month'),
        x='month',
        y='value',
        color='variable',
        title=f'Sentiment Distribution by Month',
        color_discrete_sequence=['green', 'red', 'gray']
    )
    sentiment_by_month_fig.update_layout(height=400)  # Adjust the height of the figure
    st.plotly_chart(sentiment_by_month_fig, use_container_width=True)
    st.subheader('', divider='rainbow')
    # Created with love by Michaël
    st.markdown(
        '<p style="text-align:center;">Created with ❤️ by <a href="https://www.linkedin.com/in/mscherding/" target="_blank">Michaël</a></p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()