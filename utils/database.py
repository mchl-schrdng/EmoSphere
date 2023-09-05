from datetime import datetime, timedelta
from collections import Counter
import streamlit as st
import supabase as sp

# Initialize Supabase client
url = st.secrets["SUPABASE_URL"]
api_key = st.secrets["SUPABASE_API_KEY"]
supabase_client = sp.create_client(url, api_key)

def insert_word(word: str):
    """Insère un nouveau mot dans la table user_emotions."""
    data = {"word": word}
    response = supabase_client.table("user_emotions").insert([data]).execute()
    return response

def retrieve_words(time_range):
    # Convert datetime objects to string in the format 'YYYY-MM-DD HH:MM:SS'
    start_time_str = time_range[0].strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = time_range[1].strftime('%Y-%m-%d %H:%M:%S')

    # Execute the query
    response = supabase_client.table("user_emotions").select('*').filter('created_at', 'gte', start_time_str).filter('created_at', 'lte', end_time_str).execute()

    return response

def get_word_frequencies(time_range):
    # Convert datetime objects to string in the format 'YYYY-MM-DD HH:MM:SS'
    start_time_str = time_range[0].strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = time_range[1].strftime('%Y-%m-%d %H:%M:%S')

    # Execute the query
    response = supabase_client.table("user_emotions").select('word').filter('created_at', 'gte', start_time_str).filter('created_at', 'lte', end_time_str).execute()

    # Check if the response contains data
    if response.status_code == 200 and response.data:
        # Extract the 'word' field from each record in the response
        words = [item['word'] for item in response.data]
        
        # Count the occurrences of each word
        word_frequencies = Counter(words)

        return word_frequencies
    else:
        return Counter()  # return an empty Counter object
