import os
import requests
import tempfile
import uuid

# Configure FFmpeg path BEFORE importing MoviePy to avoid blocking
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips, afx

def download_file(url, extension=".mp4"):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
        for chunk in response.iter_content(chunk_size=8192):
            tfile.write(chunk)
        tfile.close()
        return tfile.name
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def create_subtitles(script_text: str, duration: float) -> list:
    """
    Generates a list of TextClips synced to likely audio. 
    Heuristic: Split into ~5 word chunks, distribute evenly.
    """
    if not script_text:
        return []
        
    words = script_text.split()
    chunk_size = 5
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    if not chunks:
        return []

    chunk_duration = duration / len(chunks)
    clips = []
    
    for i, chunk in enumerate(chunks):
        # Create text clip
        # Font 'Liberation-Sans' is installed in Docker/System
        txt_clip = (TextClip(chunk, fontsize=40, color='white', font='Liberation-Sans-Bold', stroke_color='black', stroke_width=2, size=(720, None), method='caption')
                    .set_position(('center', 0.80), relative=True)
                    .set_duration(chunk_duration)
                    .set_start(i * chunk_duration))
        clips.append(txt_clip)
        
    return clips

def combine_audio_video(video_url: str, audio_bytes: bytes, script_text: str = "", background_music_url: str = None) -> str:
    """
    Downloads video, saves audio, merges them, adds subtitles and background music.
    """
    video_path = download_file(video_url, ".mp4")
    
    # Save audio bytes to temp file
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio.write(audio_bytes)
    temp_audio.close()
    audio_path = temp_audio.name
    
    music_path = None
    if background_music_url:
        print(f"🎵 Downloading background music: {background_music_url}")
        music_path = download_file(background_music_url, ".mp3")
        
    output_filename = f"{uuid.uuid4()}.mp4"
    # Ensure static dir exists
    os.makedirs("static", exist_ok=True)
    output_path = os.path.join("static", output_filename)

    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        print(f"DEBUG: Video Duration: {video_clip.duration}")
        print(f"DEBUG: Audio Duration: {audio_clip.duration}")
        
        # Logic: Video duration matches Audio duration (Voice)
        final_duration = audio_clip.duration
        
        if video_clip.duration < final_duration:
             # Loop video by repeating it
             num_loops = int(final_duration / video_clip.duration) + 1
             final_clip = concatenate_videoclips([video_clip] * num_loops).subclip(0, final_duration)
        else:
             # Cut video
             final_clip = video_clip.subclip(0, final_duration)

        # 4. Resize/Crop to 9:16 (Vertical) if needed
        # Assuming Pexels video is already vertical or we crop center
        w, h = final_clip.size
        target_ratio = 9/16
        if w/h > target_ratio:
            # Too wide, crop center
            new_w = h * target_ratio
            final_clip = final_clip.crop(x1=w/2 - new_w/2, width=new_w, height=h)
        
        # 5. Audio Mixing (Voice + Music)
        # Voice volume normal
        voice = audio_clip.volumex(1.0)
        
        if music_path:
            bg_music = AudioFileClip(music_path)
            # Loop music to match video
            bg_music = afx.audio_loop(bg_music, duration=final_duration)
            # Ducking: Low volume (10%)
            bg_music = bg_music.volumex(0.10)
            
            # Mix
            final_audio = CompositeAudioClip([voice, bg_music])
            final_clip = final_clip.set_audio(final_audio)
        else:
            final_clip = final_clip.set_audio(voice)
        
        # 6. Add Subtitles (Burn-in)
        if script_text:
            print("Generating subtitles...")
            try:
                subtitle_clips = create_subtitles(script_text, final_duration)
                if subtitle_clips:
                    final_clip = CompositeVideoClip([final_clip] + subtitle_clips)
            except Exception as e:
                print(f"⚠️ Failed to add subtitles: {e}")
        
        # Write File
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True, fps=24)
        
        # Cleanup
        video_clip.close()
        audio_clip.close()
        if music_path:
            os.remove(music_path)
            
        return f"http://localhost:8000/static/{output_filename}"

    except Exception as e:
        print(f"Video Editor Error: {e}")
        raise e
    finally:
        # Cleanup temp files
        if os.path.exists(video_path): os.remove(video_path)
        if os.path.exists(audio_path): os.remove(audio_path)