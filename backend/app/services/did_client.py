"""
D-ID API Client for Talking Avatar Generation with Lip-Sync
"""
import os
import time
import requests
from typing import Optional
from app.config import settings


class DIDClient:
    """Client for D-ID Talking Avatar API"""
    
    def __init__(self):
        self.api_key = os.getenv("DID_API_KEY")
        self.base_url = "https://api.d-id.com"
        
        if not self.api_key:
            print("⚠️ Warning: DID_API_KEY not found in environment")
    
    def create_talking_avatar(
        self,
        image_url: str,
        audio_url: str,
        timeout: int = 120
    ) -> Optional[str]:
        """
        Create a talking avatar video with lip-sync from image and audio.
        
        Args:
            image_url: URL of the avatar image
            audio_url: URL of the audio file
            timeout: Max wait time in seconds
            
        Returns:
            URL of the generated video or None if failed
        """
        if not self.api_key:
            print("❌ D-ID API key missing, skipping avatar generation")
            return None
        
        try:
            # Step 1: Create talk
            print(f"🎭 D-ID: Creating talking avatar...")
            
            headers = {
                "Authorization": f"Basic {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "source_url": image_url,
                "script": {
                    "type": "audio",
                    "audio_url": audio_url
                },
                "config": {
                    "fluent": True,
                    "pad_audio": 0.0,
                    "stitch": True
                }
            }
            
            # Submit request
            response = requests.post(
                f"{self.base_url}/talks",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code not in [200, 201]:
                print(f"❌ D-ID API error: {response.status_code} - {response.text}")
                return None
            
            talk_id = response.json().get("id")
            print(f"✅ D-ID talk created: {talk_id}")
            
            # Step 2: Poll for completion
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{self.base_url}/talks/{talk_id}",
                    headers=headers,
                    timeout=30
                )
                
                if status_response.status_code != 200:
                    print(f"❌ D-ID status check failed: {status_response.status_code}")
                    return None
                
                talk_data = status_response.json()
                status = talk_data.get("status")
                
                if status == "done":
                    video_url = talk_data.get("result_url")
                    print(f"✅ D-ID avatar complete: {video_url}")
                    return video_url
                
                elif status == "error":
                    error = talk_data.get("error", {}).get("description", "Unknown error")
                    print(f"❌ D-ID generation failed: {error}")
                    return None
                
                elif status in ["created", "started"]:
                    print(f"⏳ D-ID processing...")
                    time.sleep(5)  # Poll every 5 seconds
                
                else:
                    print(f"⚠️ Unknown D-ID status: {status}")
                    time.sleep(5)
            
            print(f"⏱️ D-ID timeout after {timeout}s")
            return None
            
        except Exception as e:
            print(f"❌ D-ID exception: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def estimate_cost(self, duration: int) -> float:
        """
        Estimate cost for avatar generation.
        
        Args:
            duration: Video duration in seconds
            
        Returns:
            Estimated cost in USD
        """
        # D-ID: ~$0.10 per 20 seconds
        return (duration / 20) * 0.10


# Singleton instance
did_client = DIDClient()
