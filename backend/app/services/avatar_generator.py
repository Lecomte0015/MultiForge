"""
Avatar Generator using DALL-E 3
"""
import os
import requests
from typing import Optional
from app.config import settings


class AvatarGenerator:
    """Generate avatar images using DALL-E 3"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            print("⚠️ Warning: OPENAI_API_KEY not found in environment")
    
    def generate_avatar(
        self,
        description: str,
        style: str = "photorealistic"
    ) -> Optional[str]:
        """
        Generate an avatar image using DALL-E 3.
        
        Args:
            description: Description of the avatar to generate
            style: Style of the image (photorealistic, cartoon, etc.)
            
        Returns:
            URL of the generated image or None if failed
        """
        if not self.api_key:
            print("❌ OpenAI API key missing, skipping avatar generation")
            return None
        
        try:
            print(f"🎨 DALL-E 3: Generating avatar '{description[:50]}...'")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Enhance prompt for better avatar quality
            enhanced_prompt = f"Professional {style} portrait photo of {description}. High quality, well-lit, clear face, studio photography, 4K resolution."
            
            payload = {
                "model": "dall-e-3",
                "prompt": enhanced_prompt,
                "size": "1024x1024",
                "quality": "hd",
                "n": 1
            }
            
            response = requests.post(
                f"{self.base_url}/images/generations",
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"❌ DALL-E 3 API error: {response.status_code} - {response.text}")
                return None
            
            image_url = response.json()["data"][0]["url"]
            print(f"✅ DALL-E 3 avatar generated: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ DALL-E 3 exception: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def estimate_cost(self) -> float:
        """
        Estimate cost for avatar generation.
        
        Returns:
            Estimated cost in USD
        """
        # DALL-E 3 HD: $0.08 per image
        return 0.08


# Singleton instance
avatar_generator = AvatarGenerator()
