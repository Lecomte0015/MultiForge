"""
Storage utilities for uploading files to Supabase Storage
"""
import os
from app.services.db_client import supabase_client
import uuid


def upload_audio_to_storage(audio_bytes: bytes, filename: str = None) -> str:
    """
    Upload audio bytes to Supabase Storage and return public URL.
    
    Args:
        audio_bytes: Audio file bytes
        filename: Optional filename (will generate UUID if not provided)
        
    Returns:
        Public URL of uploaded audio file
    """
    try:
        if not filename:
            filename = f"{uuid.uuid4()}.mp3"
        
        # Upload to Supabase Storage
        bucket_name = "audio-files"
        
        # Create bucket if it doesn't exist (first time only)
        try:
            supabase_client.storage.create_bucket(bucket_name, {"public": True})
        except:
            pass  # Bucket already exists
        
        # Upload file
        supabase_client.storage.from_(bucket_name).upload(
            filename,
            audio_bytes,
            {"content-type": "audio/mpeg"}
        )
        
        # Get public URL
        public_url = supabase_client.storage.from_(bucket_name).get_public_url(filename)
        
        return public_url
        
    except Exception as e:
        print(f"Error uploading audio to storage: {e}")
        return None


def upload_image_to_storage(image_url: str, filename: str = None) -> str:
    """
    Download image from URL and upload to Supabase Storage.
    
    Args:
        image_url: URL of image to download
        filename: Optional filename
        
    Returns:
        Public URL of uploaded image
    """
    try:
        import requests
        
        if not filename:
            filename = f"{uuid.uuid4()}.jpg"
        
        # Download image
        response = requests.get(image_url, timeout=30)
        if response.status_code != 200:
            return None
        
        image_bytes = response.content
        
        # Upload to Supabase Storage
        bucket_name = "avatar-images"
        
        # Create bucket if it doesn't exist
        try:
            supabase_client.storage.create_bucket(bucket_name, {"public": True})
        except:
            pass
        
        # Upload file
        supabase_client.storage.from_(bucket_name).upload(
            filename,
            image_bytes,
            {"content-type": "image/jpeg"}
        )
        
        # Get public URL
        public_url = supabase_client.storage.from_(bucket_name).get_public_url(filename)
        
        return public_url
        
    except Exception as e:
        print(f"Error uploading image to storage: {e}")
        return None
