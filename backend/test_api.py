import sys
import os
from dotenv import load_dotenv

# Load env vars from .env file
load_dotenv()

# Add current dir to path so we can import app
sys.path.append(os.getcwd())

from app.workers.job_pipeline import run_pipeline
from app.config import settings

def mock_progress(percent, message, logs):
    print(f"[{percent}%] {message}")
    if logs:
        print(f"  Last Log: {logs[-1]}")

def test_integration():
    print(f"--- Starting Integration Test ---")
    print(f"Mock Mode: {settings.MOCK_MODE}")
    print(f"OpenAI Key Present: {bool(settings.OPENAI_API_KEY)}")
    print(f"Pexels Key Present: {bool(settings.PEXELS_API_KEY)}")
    print(f"ElevenLabs Key Present: {bool(settings.ELEVENLABS_API_KEY)}")
    
    data = {
        "topic": "The future of AI in 2025",
        "visual_style": "futuristic",
        "platform": "tiktok"
    }
    
    try:
        result = run_pipeline(data, mock_progress)
        print("\n--- Test Success ---")
        print(f"Video URL: {result['result_video_url']}")
        print(f"Script Length: {len(result['script_text'])} chars")
    except Exception as e:
        print("\n--- Test Failed ---")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integration()
