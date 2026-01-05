import time
import random
import requests
import os
import json
import re
from app.config import settings
from app.services.video_editor import combine_audio_video
from app.services.db_client import supabase_client

def clean_script_for_tts(script_text):
    """
    Enlève les métadonnées markdown du script avant TTS.
    """
    import re
    # Enlever tout ce qui est entre ** ** (titres, labels)
    cleaned = re.sub(r'\*\*[^*]+\*\*', '', script_text)
    # Enlever les timecodes (0-3s), (3-40s), etc.
    cleaned = re.sub(r'\([\d\s-]+s\)', '', cleaned)
    # Enlever les deux-points orphelins
    cleaned = re.sub(r':\s*\n', '\n', cleaned)
    # Enlever les lignes vides multiples
    cleaned = re.sub(r'\n\s*\n+', ' ', cleaned)
    # Enlever les emojis et caractères spéciaux
    cleaned = re.sub(r'[🎬🧠🎙️🖼️🎵📹💾✅⚠️❌]', '', cleaned)
    return cleaned.strip()

# --- Constants ---
MOCK_VIDEO_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB" 
DEFAULT_MUSIC = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"

def run_pipeline(data: dict, progress_callback):
    """
    Pipeline FACELESS avec Persistance DB (Supabase)
    """
    mock_mode = settings.MOCK_MODE
    logs = []
    
    topic = data.get('topic', 'No Topic')
    user_script = data.get('script')
    visual_style = data.get('visual_style', 'cinematic')
    user_id = data.get('user_id') # <--- On récupère l'ID utilisateur
    
    logs.append(f"🚀 Démarrage Job (Mock={mock_mode}, User={user_id})")

    # --- Étape 1 : Script ---
    script = ""
    if user_script:
        logs.append("📝 Script fourni.")
        script = user_script
        progress_callback(10, "Validation...", logs)
    else:
        logs.append(f"🧠 Génération Script IA sur : {topic}")
        progress_callback(5, "Rédaction IA...", logs)
        if mock_mode:
            time.sleep(1)
            script = f"Ceci est un script de test sur {topic}."
        else:
            try:
                openai_url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                payload = {
                    "model": "gpt-4-turbo-preview",
                    "messages": [
                        {"role": "system", "content": "You are a viral scriptwriter for TikTok. Write a 3-part script (Hook, Body, CTA) about the given topic. Keep it under 60 seconds spoken. Return ONLY the text, no markdown headers."},
                        {"role": "user", "content": topic}
                    ]
                }
                res = requests.post(openai_url, json=payload, headers=headers)
                if res.status_code == 200:
                    script = res.json()['choices'][0]['message']['content']
                    logs.append("✅ Script GPT-4 OK.")
                else:
                    raise Exception(f"OpenAI: {res.text}")
            except Exception as e:
                logs.append(f"❌ Err Script: {e}")
                script = f"Script fallback {topic}"

    # --- Étape 2 : Director Mode ---
    logs.append(f"🎬 Director Mode ({visual_style})...")
    progress_callback(20, "Analyse Visuelle...", logs)
    keywords = [str(topic).split()[0]]
    if not mock_mode:
        try:
            openai_url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            payload = {
                "model": "gpt-4-turbo-preview",
                "messages": [
                    {"role": "system", "content": "You are a video director. Extract 3 CONCRETE, VISUAL search terms from this script for stock footage. Focus on emotions, actions, or objects that can be filmed. Avoid abstract concepts. Return ONLY the terms separated by commas, in English."},
                    {"role": "user", "content": f"Script: {script}\nStyle: {visual_style}"}
                ]
            }
            res = requests.post(openai_url, json=payload, headers=headers)
            if res.status_code == 200:
                keywords = [k.strip() for k in res.json()['choices'][0]['message']['content'].split(',')]
                logs.append(f"🧠 Mots-clés IA: {keywords}")
        except Exception as e:
            import traceback
            logs.append(f"⚠️ Fallback Director: {e}")
            logs.append(f"DEBUG Traceback: {traceback.format_exc()}")

    # --- Étape 3 : Audio (TTS) ---
    logs.append("🎙️ Audio (ElevenLabs)...")
    progress_callback(40, "Synthèse Vocale...", logs)
    audio_bytes = None
    if not mock_mode:
        try:
            # Extract voice script from complex prompt
            from app.services.script_extractor import extract_voice_script
            voice_script = extract_voice_script(data.get('topic', script))
            logs.append(f"🧠 Script extrait: {len(voice_script)} caractères")
            
            tts_text = clean_script_for_tts(voice_script) # Nettoyage !
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{data.get('voice_id', DEFAULT_VOICE_ID)}"
            headers = {"xi-api-key": settings.ELEVENLABS_API_KEY, "Content-Type": "application/json"}
            payload = {
                "text": tts_text, 
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            res = requests.post(url, json=payload, headers=headers)
            if res.status_code == 200:
                audio_bytes = res.content
                logs.append("✅ Audio OK.")
            else:
                 raise Exception(f"ElevenLabs: {res.text}")
        except Exception as e:
             logs.append(f"❌ Err Audio: {e}")

    # --- Étape 4 : Visuels (Hybride: Pexels + Runway) ---
    logs.append("🖼️ Acquisition Visuels (Hybride)...")
    progress_callback(60, "Acquisition Visuels...", logs)
    found_videos = []
    
    if not mock_mode:
        try:
            # Import hybrid router
            from app.services.video_source_router import video_router
            
            # Classify scenes with GPT-4
            scenes = video_router.classify_scenes(script)
            logs.append(f"🧠 {len(scenes)} scènes classifiées")
            
            # Estimate cost
            estimated_cost = video_router.estimate_cost(scenes)
            if estimated_cost > 0:
                logs.append(f"💰 Coût estimé Runway: ${estimated_cost:.2f}")
            
            # Get videos for each scene
            for i, scene in enumerate(scenes[:3]):  # Max 3 scenes for now
                scene_text = scene.get("text", "")
                source = scene.get("source", "stock")
                
                logs.append(f"🎬 Scène {i+1}: {scene_text[:40]}... ({source})")
                
                video_url = video_router.get_video(scene)
                if video_url:
                    found_videos.append(video_url)
                    logs.append(f"✅ Vidéo {i+1} acquise")
                else:
                    logs.append(f"⚠️ Échec scène {i+1}")
            
        except Exception as e:
            logs.append(f"❌ Err Visuels: {e}")
            import traceback
            print(f"Video acquisition error: {traceback.format_exc()}")

    # --- Étape 5 : Montage ---
    logs.append("🎞️ Montage & Mixage...")
    progress_callback(80, "Rendu final...", logs)
    final_video = MOCK_VIDEO_URL
    
    try:
        vid_src = found_videos[0] if found_videos else MOCK_VIDEO_URL
        if not mock_mode:
            if audio_bytes:
                # TOUJOURS générer avec sous-titres
                final_video = combine_audio_video(vid_src, audio_bytes, clean_script_for_tts(script), DEFAULT_MUSIC)
                logs.append(f"✅ Vidéo Générée: {final_video}")
            else:
                final_video = vid_src 
    except Exception as e:
        logs.append(f"❌ Err Montage: {e}")

    # --- Étape 6 : Persistance (Supabase) ---
    if supabase_client and user_id:
        logs.append("💾 Sauvegarde DB...")
        try:
            project_data = {
                "name": topic,
                "description": script[:100] + "...",
                "status": "completed",
                "user_id": user_id,
                "settings": {
                    "video_url": final_video,
                    "script": script,
                    "style": visual_style,
                    "keywords": keywords
                }
            }
            supabase_client.table("projects").insert(project_data).execute()
            logs.append("✅ Projet sauvegardé dans le Dashboard !")
        except Exception as e:
             logs.append(f"⚠️ Erreur Sauvegarde: {e}")
    elif not user_id:
        logs.append("⚠️ Pas d'User ID, pas de sauvegarde.")

    progress_callback(100, "Terminé", logs)
    return {
        "status": "COMPLETED",
        "result_video_url": final_video, 
        "script_text": script,
        "logs": logs
    }