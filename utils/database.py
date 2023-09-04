from supabase_py import create_client, Client

# Initialize Supabase client
url: str = "your-supabase-url"
api_key: str = "your-supabase-api-key"
supabase: Client = create_client(url, api_key)

def insert_word(word: str):
    # Insert word into the 'words' table
    supabase.table('words').insert({"word": word}).execute()
