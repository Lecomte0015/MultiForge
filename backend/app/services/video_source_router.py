"""
Video Source Router - Intelligent routing between Pexels and Runway Gen-2
"""
import os
import requests
from typing import Dict, List, Optional
from app.config import settings
from app.services.runway_client import runway_client


class VideoSourceRouter:
    """Routes video requests to appropriate source (Pexels or Runway)"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
    
    def classify_scenes(self, script: str) -> List[Dict]:
        """
        Use GPT-4 to break script into scenes and classify each.
        
        Args:
            script: Full video script
            
        Returns:
            List of scenes with classification:
            [
                {
                    "text": "Scene description",
                    "duration": 5,
                    "source": "stock" | "generate" | "hybrid"
                }
            ]
        """
        if not self.openai_api_key:
            print("⚠️ OpenAI API key missing, using fallback classification")
            return self._fallback_classification(script)
        
        try:
            print("🧠 Classifying scenes with GPT-4...")
            
            prompt = f"""Analyze this video script and break it into 3-5 visual scenes.
For each scene, determine if it can be found as stock footage ("stock") or needs AI generation ("generate").

Use "stock" for:
- Generic scenes: nature, cities, people, common objects
- Simple actions: walking, working, eating
- B-roll footage

Use "generate" for:
- Abstract concepts: success, innovation, dreams
- Specific scenarios not available in stock
- Unique or impossible scenes

Return ONLY a JSON array like this:
[
    {{"text": "sunrise over ocean", "duration": 5, "source": "stock"}},
    {{"text": "person transforming dreams into reality", "duration": 8, "source": "generate"}},
    {{"text": "team working together", "duration": 7, "source": "stock"}}
]

Script:
{script}
"""
            
            headers = {"Authorization": f"Bearer {self.openai_api_key}"}
            payload = {
                "model": "gpt-4-turbo-preview",
                "messages": [
                    {"role": "system", "content": "You are a video production expert. Return ONLY valid JSON, no markdown."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Remove markdown code blocks if present
                content = content.replace("```json", "").replace("```", "").strip()
                
                import json
                scenes = json.loads(content)
                print(f"✅ Classified {len(scenes)} scenes")
                return scenes
            else:
                print(f"❌ GPT-4 classification failed: {response.status_code}")
                return self._fallback_classification(script)
                
        except Exception as e:
            print(f"❌ Scene classification error: {e}")
            return self._fallback_classification(script)
    
    def _fallback_classification(self, script: str) -> List[Dict]:
        """Simple fallback: treat entire script as one stock scene"""
        return [{
            "text": script[:200],  # First 200 chars
            "duration": 10,
            "source": "stock"
        }]
    
    def get_video(self, scene: Dict) -> Optional[str]:
        """
        Get video for a scene from appropriate source.
        
        Args:
            scene: Scene dict with 'text', 'duration', 'source'
            
        Returns:
            URL of video or None
        """
        source = scene.get("source", "stock")
        text = scene.get("text", "")
        duration = scene.get("duration", 5)
        
        if source == "generate":
            # Try Runway first
            print(f"🎬 Generating AI video: '{text[:50]}...'")
            video_url = runway_client.generate_video(text, duration)
            
            if video_url:
                return video_url
            else:
                # Fallback to Pexels if Runway fails
                print("⚠️ Runway failed, falling back to Pexels")
                return self._get_pexels_video(text)
        
        elif source == "hybrid":
            # Try Pexels first, Runway as fallback
            video_url = self._get_pexels_video(text)
            if video_url:
                return video_url
            else:
                print("⚠️ Pexels empty, trying Runway")
                return runway_client.generate_video(text, duration)
        
        else:  # source == "stock"
            return self._get_pexels_video(text)
    
    def _get_pexels_video(self, query: str) -> Optional[str]:
        """Search Pexels for stock video"""
        if not self.pexels_api_key:
            print("⚠️ Pexels API key missing")
            return None
        
        try:
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
            headers = {"Authorization": self.pexels_api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                videos = response.json().get('videos', [])
                if videos and videos[0].get('video_files'):
                    video_files = videos[0]['video_files']
                    # Get HD quality
                    hd_video = next((v for v in video_files if v.get('quality') == 'hd'), video_files[0])
                    return hd_video['link']
            
            return None
            
        except Exception as e:
            print(f"❌ Pexels error: {e}")
            return None
    
    def estimate_cost(self, scenes: List[Dict]) -> float:
        """
        Estimate total cost for all scenes.
        
        Args:
            scenes: List of classified scenes
            
        Returns:
            Total estimated cost in USD
        """
        total_cost = 0.0
        
        for scene in scenes:
            if scene.get("source") == "generate":
                duration = scene.get("duration", 5)
                total_cost += runway_client.estimate_cost(duration)
        
        return total_cost


# Singleton instance
video_router = VideoSourceRouter()
