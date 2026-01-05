"""
YouTube to TikTok Repurposing Pipeline
Orchestrates the complete workflow from YouTube URL to TikTok clips
"""
from typing import List, Dict, Optional
import os
import tempfile
from app.services.youtube_downloader import youtube_downloader
from app.services.transcription_service import transcription_service
from app.services.viral_moment_analyzer import viral_moment_analyzer
from app.services.clip_extractor import clip_extractor


class YouTubeRepurposingPipeline:
    """Complete pipeline for YouTube → TikTok/Shorts repurposing"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def repurpose_video(
        self,
        youtube_url: str,
        max_clips: int = 5,
        format_type: str = "vertical",
        min_duration: int = 15,
        max_duration: int = 60
    ) -> Dict:
        """
        Complete repurposing workflow
        
        Args:
            youtube_url: YouTube video URL
            max_clips: Maximum number of clips to generate
            format_type: 'vertical', 'square', or 'horizontal'
            min_duration: Minimum clip duration in seconds
            max_duration: Maximum clip duration in seconds
            
        Returns:
            {
                'success': bool,
                'video_title': str,
                'clips': [
                    {
                        'path': str,
                        'start': float,
                        'end': float,
                        'score': int,
                        'hook': str,
                        'reason': str
                    }
                ],
                'logs': [str]
            }
        """
        logs = []
        
        try:
            logs.append(f"🎬 Starting YouTube → TikTok repurposing")
            logs.append(f"URL: {youtube_url}")
            
            # Step 1: Download YouTube video
            logs.append("📥 Step 1/5: Downloading YouTube video...")
            video_data = youtube_downloader.download_video(youtube_url)
            
            if not video_data:
                return {
                    'success': False,
                    'error': 'Failed to download YouTube video',
                    'logs': logs
                }
            
            logs.append(f"✅ Downloaded: {video_data['title']}")
            logs.append(f"   Duration: {video_data['duration']}s")
            
            # Step 2: Transcribe audio
            logs.append("🎤 Step 2/5: Transcribing audio with Whisper...")
            segments = transcription_service.transcribe(video_data['audio_path'])
            
            if not segments:
                return {
                    'success': False,
                    'error': 'Failed to transcribe audio',
                    'logs': logs
                }
            
            logs.append(f"✅ Transcribed: {len(segments)} segments")
            
            # Step 3: Analyze viral moments
            logs.append("🧠 Step 3/5: Analyzing viral moments with GPT-4...")
            moments = viral_moment_analyzer.analyze_transcript(
                segments,
                max_clips=max_clips,
                min_duration=min_duration,
                max_duration=max_duration
            )
            
            if not moments:
                return {
                    'success': False,
                    'error': 'No viral moments found',
                    'logs': logs
                }
            
            logs.append(f"✅ Found {len(moments)} viral moments")
            for i, moment in enumerate(moments[:3], 1):
                logs.append(f"   {i}. Score {moment['score']}: {moment['hook']}")
            
            # Step 4: Extract clips
            logs.append(f"✂️ Step 4/5: Extracting {len(moments)} clips...")
            output_dir = os.path.join(self.temp_dir, 'clips')
            
            clip_paths = clip_extractor.extract_multiple_clips(
                video_path=video_data['video_path'],
                moments=moments,
                output_dir=output_dir,
                format_type=format_type
            )
            
            if not clip_paths:
                return {
                    'success': False,
                    'error': 'Failed to extract clips',
                    'logs': logs
                }
            
            logs.append(f"✅ Extracted {len(clip_paths)} clips")
            
            # Step 5: Prepare results
            logs.append("📦 Step 5/5: Preparing results...")
            
            clips_data = []
            for i, (clip_path, moment) in enumerate(zip(clip_paths, moments)):
                clips_data.append({
                    'path': clip_path,
                    'filename': os.path.basename(clip_path),
                    'start': moment['start'],
                    'end': moment['end'],
                    'duration': moment['end'] - moment['start'],
                    'score': moment['score'],
                    'hook': moment['hook'],
                    'reason': moment['reason'],
                    'text': moment.get('text', '')
                })
            
            logs.append(f"✅ Repurposing complete!")
            logs.append(f"   Generated {len(clips_data)} TikTok/Shorts clips")
            
            return {
                'success': True,
                'video_title': video_data['title'],
                'video_duration': video_data['duration'],
                'clips': clips_data,
                'logs': logs
            }
            
        except Exception as e:
            logs.append(f"❌ Pipeline error: {e}")
            import traceback
            logs.append(traceback.format_exc())
            
            return {
                'success': False,
                'error': str(e),
                'logs': logs
            }


# Singleton instance
youtube_repurposing_pipeline = YouTubeRepurposingPipeline()
