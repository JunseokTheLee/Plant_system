import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_SUPABASE_URL = os.environ.get("SUPABASE_URL")
_SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

_client: Client | None = None
IMAGE_BUCKET = "plant-images"


def get_client() -> Client:
    global _client
    if _client is None:
        if not _SUPABASE_URL or not _SUPABASE_ANON_KEY:
            raise RuntimeError(
                "SUPABASE_URL / SUPABASE_ANON_KEY not set. Copy .env.example to .env "
                "and fill in your project's values."
            )
        _client = create_client(_SUPABASE_URL, _SUPABASE_ANON_KEY)
    return _client


def fetch_plants() -> list[dict]:
    res = get_client().table("plants").select("*").order("created_at").execute()
    return res.data


def insert_plant(name: str, status: str = "Unknown", description: str = "",
                  image_path: str | None = None) -> dict:
    row = {
        "name": name,
        "status": status,
        "description": description,
        "image_path": image_path,
    }
    res = get_client().table("plants").insert(row).execute()
    return res.data[0]


def update_plant(plant_id: str, **fields) -> dict:
    res = get_client().table("plants").update(fields).eq("id", plant_id).execute()
    return res.data[0]


def upload_image(local_path: str) -> str:
    """Uploads a local image to Supabase Storage and returns its public URL."""
    path = Path(local_path)
    dest_name = f"{os.urandom(8).hex()}_{path.name}"

    with open(local_path, "rb") as f:
        get_client().storage.from_(IMAGE_BUCKET).upload(
            dest_name, f, {"content-type": _guess_content_type(path.suffix)}
        )

    return get_client().storage.from_(IMAGE_BUCKET).get_public_url(dest_name)


def _guess_content_type(suffix: str) -> str:
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".bmp": "image/bmp",
    }.get(suffix.lower(), "application/octet-stream")
