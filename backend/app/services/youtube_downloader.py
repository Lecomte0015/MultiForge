"""
YouTube Video Downloader Service
Downloads videos from YouTube using yt-dlp
"""
import yt_dlp
import os
from typing import Dict, Optional
import tempfile


class YouTubeDownloader:
    """Service for downloading YouTube videos"""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize YouTube downloader
        
        Args:
            output_dir: Directory to save downloaded videos (default: temp)
        """
        self.output_dir = output_dir or tempfile.mkdtemp()
        os.makedirs(self.output_dir, exist_ok=True)
    
    def download_video(self, url: str) -> Optional[Dict]:
        """
        Download YouTube video
        
        Args:
            url: YouTube video URL
            
        Returns:
            {
                'video_path': str,
                'audio_path': str,
                'duration': float,
                'title': str,
                'thumbnail': str,
                'id': str
            }
        """
        try:
            print(f"📥 Downloading YouTube video: {url}")
            
            ydl_opts = {
                'format': 'best[height<=1080]',  # Max 1080p
                'outtmpl': f'{self.output_dir}/%(id)s.%(ext)s',
                'writesubtitles': False,
                'writeautomaticsub': False,
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info without downloading first
                info = ydl.extract_info(url, download=False)
                
                # Check duration (max 30 minutes)
                duration = info.get('duration', 0)
                if duration > 1800:  # 30 minutes
                    print(f"⚠️ Video too long: {duration}s (max 1800s)")
                    return None
                
                # Download video
                info = ydl.extract_info(url, download=True)
                
                video_path = ydl.prepare_filename(info)
                
                # Extract audio separately
                audio_path = self._extract_audio(video_path)
                
                result = {
                    'video_path': video_path,
                    'audio_path': audio_path,
                    'duration': duration,
                    'title': info.get('title', 'Unknown'),
                    'thumbnail': info.get('thumbnail', ''),
                    'id': info.get('id', '')
                }
                
                print(f"✅ Downloaded: {result['title']} ({duration}s)")
                return result
                
        except Exception as e:
            print(f"❌ YouTube download error: {e}")
            return None
    
    def _extract_audio(self, video_path: str) -> str:
        """
        Extract audio from video
        
        Args:
            video_path: Path to video file
            
        Returns:
            Path to extracted audio file
        """
        try:
            from moviepy.editor import VideoFileClip
            
            audio_path = video_path.rsplit('.', 1)[0] + '_audio.mp3'
            
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, logger=None)
            video.close()
            
            return audio_path
            
        except Exception as e:
            print(f"⚠️ Audio extraction error: {e}")
            # Return video path as fallback
            return video_path


# Singleton instance
youtube_downloader = YouTubeDownloader()
