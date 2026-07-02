import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
def upload_screenshot(file_path):
    file_name = os.path.basename(file_path)
    storage_path = f"public/{file_name}"
    with open(file_path, "rb") as file:

        supabase.storage.from_("screenshots").upload(
            path=storage_path,
            file=file,
            file_options={"content-type": "image/jpeg"}
    )
    public_url = supabase.storage.from_("screenshots").get_public_url(storage_path)
    return public_url