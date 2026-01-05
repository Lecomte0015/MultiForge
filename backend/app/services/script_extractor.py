"""
Script Extraction Utilities
"""
import os
import requests
from typing import Optional
from app.config import settings


def extract_voice_script(prompt: str) -> str:
    """
    Extract only the voice script from a complex prompt using GPT-4.
    
    Handles prompts that contain:
    - Instructions for video creation
    - Visual descriptions
    - Voice script sections
    - Timing information
    - Technical specifications
    
    Returns only the text that should be spoken by the voice.
    
    Args:
        prompt: Full user prompt with all instructions
        
    Returns:
        Extracted voice script, or original prompt if extraction fails
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️ OpenAI API key missing, using full prompt")
        return prompt
    
    try:
        print("🧠 Extracting voice script from prompt...")
        
        extraction_prompt = f"""Extract ONLY the voice script from this prompt. 
Return ONLY the text that should be spoken aloud, removing:
- Video creation instructions
- Visual descriptions  
- Technical specifications
- Timing markers like (0-4s)
- Section headers like "Intro", "Body", "CTA"
- Emojis and special characters

If there's a clear "SCRIPT VOIX" or similar section, extract only that.
If the entire prompt is a voice script, return it cleaned up.
Return ONLY the speaking text, nothing else.

Prompt:
{prompt}

Voice Script:"""
        
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "gpt-4-turbo-preview",
            "messages": [
                {"role": "system", "content": "You are a script extraction expert. Return ONLY the voice script text, nothing else."},
                {"role": "user", "content": extraction_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            extracted = response.json()['choices'][0]['message']['content'].strip()
            print(f"✅ Script extracted: {len(extracted)} characters")
            return extracted
        else:
            print(f"❌ Extraction failed: {response.status_code}")
            return prompt
            
    except Exception as e:
        print(f"❌ Script extraction error: {e}")
        return prompt


def extract_avatar_description(prompt: str) -> Optional[str]:
    """
    Extract avatar/character description from prompt using GPT-4.
    
    Args:
        prompt: Full user prompt
        
    Returns:
        Avatar description for image generation, or None
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return None
    
    try:
        print("🎨 Extracting avatar description...")
        
        extraction_prompt = f"""Extract a description of the character/avatar from this prompt.
Return a concise description suitable for image generation (DALL-E 3).
Focus on:
- Physical appearance
- Clothing/accessories
- Setting/environment
- Style (photorealistic, cartoon, etc.)

If no character is described, return "NONE".

Prompt:
{prompt}

Avatar Description:"""
        
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "gpt-4-turbo-preview",
            "messages": [
                {"role": "system", "content": "You are an image prompt expert. Return a concise avatar description or 'NONE'."},
                {"role": "user", "content": extraction_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 200
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            description = response.json()['choices'][0]['message']['content'].strip()
            if description.upper() == "NONE":
                return None
            print(f"✅ Avatar description: {description[:50]}...")
            return description
        else:
            return None
            
    except Exception as e:
        print(f"❌ Avatar extraction error: {e}")
        return None
