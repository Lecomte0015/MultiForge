"""
Runway Gen-4 API Client for AI Video Generation
"""
import os
import time
import requests
from typing import Optional
from app.config import settings


class RunwayClient:
    """Client for Runway Gen-4 API"""
    
    def __init__(self):
        self.api_key = os.getenv("RUNWAY_API_KEY")
        self.base_url = "https://api.dev.runwayml.com/v1"
        
        if not self.api_key:
            print("⚠️ Warning: RUNWAY_API_KEY not found in environment")
    
    def generate_video(
        self, 
        prompt: str, 
        duration: int = 5,
        aspect_ratio: str = "9:16",
        timeout: int = 180
    ) -> Optional[str]:
        """
        Generate a video from text prompt using Runway Gen-4.
        
        Args:
            prompt: Text description of the video to generate
            duration: Video duration in seconds (2-10)
            aspect_ratio: Video aspect ratio (9:16 for vertical)
            timeout: Max wait time in seconds
            
        Returns:
            URL of the generated video or None if failed
        """
        if not self.api_key:
            print("❌ Runway API key missing, skipping generation")
            return None
        
        try:
            # Step 1: Submit generation request
            print(f"🎬 Runway: Generating '{prompt[:50]}...' ({duration}s)")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06"
            }
            
            # Convert aspect_ratio format to valid ratios
            ratio_map = {
                "9:16": "720:1280",
                "16:9": "1280:720",
                "1:1": "1080:1920"  # Using vertical as default for 1:1
            }
            ratio = ratio_map.get(aspect_ratio, "720:1280")
            
            # Duration must be exactly 4, 6, or 8 seconds for veo3.1_fast
            valid_durations = [4, 6, 8]
            actual_duration = min(valid_durations, key=lambda x: abs(x - duration))
            
            payload = {
                "promptText": prompt,
                "model": "veo3.1_fast",  # Fastest model available
                "ratio": ratio,
                "duration": actual_duration
            }
            
            # Submit request
            response = requests.post(
                f"{self.base_url}/text_to_video",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ Runway API error: {response.status_code} - {response.text}")
                return None
            
            task_id = response.json().get("id")
            print(f"✅ Runway task created: {task_id}")
            
            # Step 2: Poll for completion
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{self.base_url}/tasks/{task_id}",
                    headers=headers,
                    timeout=30
                )
                
                if status_response.status_code != 200:
                    print(f"❌ Runway status check failed: {status_response.status_code}")
                    return None
                
                task_data = status_response.json()
                status = task_data.get("status")
                
                if status == "SUCCEEDED":
                    # Get video URL from artifacts
                    artifacts = task_data.get("artifacts", [])
                    if artifacts and len(artifacts) > 0:
                        video_url = artifacts[0].get("url")
                        print(f"✅ Runway generation complete: {video_url}")
                        return video_url
                    else:
                        # Try alternative paths - output is a list
                        output = task_data.get("output")
                        if output and isinstance(output, list) and len(output) > 0:
                            video_url = output[0]
                            print(f"✅ Runway generation complete: {video_url}")
                            return video_url
                        elif output and isinstance(output, str):
                            print(f"✅ Runway generation complete: {output}")
                            return output
                        
                        print(f"❌ No video URL in response. Keys: {list(task_data.keys())}")
                        return None
                
                elif status == "FAILED":
                    failure = task_data.get("failure")
                    print(f"❌ Runway generation failed: {failure}")
                    return None
                
                elif status in ["PENDING", "RUNNING"]:
                    progress = task_data.get("progress", 0)
                    print(f"⏳ Runway progress: {int(progress * 100)}%")
                    time.sleep(10)  # Poll every 10 seconds
                
                else:
                    print(f"⚠️ Unknown Runway status: {status}")
                    time.sleep(10)
            
            print(f"⏱️ Runway timeout after {timeout}s")
            return None
            
        except Exception as e:
            print(f"❌ Runway exception: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def estimate_cost(self, duration: int) -> float:
        """
        Estimate cost for video generation.
        
        Args:
            duration: Video duration in seconds
            
        Returns:
            Estimated cost in USD
        """
        # Gen-4 Turbo: ~$0.05/second
        return duration * 0.05


# Singleton instance
runway_client = RunwayClient()
