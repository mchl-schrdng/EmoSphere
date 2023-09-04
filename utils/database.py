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
    """Récupère les mots de la table user_emotions en fonction d'une plage de temps sélectionnée."""
    start_time, end_time = time_range
    response = supabase_client.table("user_emotions").select('*').filter('created_at', 'gte', start_time).filter('created_at', 'lte', end_time).execute()
    return response
