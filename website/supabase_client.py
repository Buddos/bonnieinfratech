import os
from django.conf import settings
from supabase import create_client, Client

_supabase_client = None

def get_supabase_client() -> Client:
    """
    Returns an initialized Supabase Python client instance using
    SUPABASE_URL and SUPABASE_KEY defined in Django settings or environment.
    """
    global _supabase_client
    if _supabase_client is None:
        url = getattr(settings, 'SUPABASE_URL', None) or os.environ.get('SUPABASE_URL')
        key = getattr(settings, 'SUPABASE_KEY', None) or os.environ.get('SUPABASE_KEY')

        if not url or not key:
            raise ValueError(
                "Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY in your .env file."
            )
        _supabase_client = create_client(url, key)
    return _supabase_client
