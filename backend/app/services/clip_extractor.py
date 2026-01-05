"""
Clip Extractor Service
Extracts and reformats video clips for TikTok/Shorts
"""
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import cv2
import numpy as np
from typing import Dict, Optional, List
import os


class ClipExtractor:
    """Service for extracting and reformatting video clips"""
    
    def __init__(self):
        self.target_formats = {
            'vertical': (1080, 1920),    # 9:16 TikTok/Shorts
            'square': (1080, 1080),      # 1:1 Instagram
            'horizontal': (1920, 1080)   # 16:9 YouTube
        }
    
    def extract_clip(
        self,
        video_path: str,
        start: float,
        end: float,
        output_path: str,
        format_type: str = "vertical",
        add_subtitles: bool = True,
        subtitle_text: str = None
    ) -> Optional[str]:
        """
        Extract and reformat video clip
        
        Args:
            video_path: Path to source video
            start: Start time in seconds
            end: End time in seconds
            output_path: Path for output clip
            format_type: 'vertical', 'square', or 'horizontal'
            add_subtitles: Whether to add subtitles
            subtitle_text: Text for subtitles
            
        Returns:
            Path to generated clip or None
        """
        try:
            print(f"✂️ Extracting clip: {start:.1f}s - {end:.1f}s")
            
            # Load and extract clip
            video = VideoFileClip(video_path)
            clip = video.subclip(start, end)
            
            # Reformat based on target format
            if format_type == "vertical":
                clip = self._smart_crop_vertical(clip)
            elif format_type == "square":
                clip = self._smart_crop_square(clip)
            # horizontal stays as is
            
            # Add subtitles if requested
            if add_subtitles and subtitle_text:
                clip = self._add_tiktok_subtitles(clip, subtitle_text)
            
            # Export optimized for TikTok/Shorts
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=30,
                preset='medium',
                bitrate='5000k',
                logger=None  # Suppress MoviePy logs
            )
            
            # Cleanup
            clip.close()
            video.close()
            
            print(f"✅ Clip extracted: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Clip extraction error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _smart_crop_vertical(self, clip):
        """
        Smart crop to 9:16 vertical format (1080x1920)
        Centers on the most important content
        """
        w, h = clip.size
        target_w, target_h = self.target_formats['vertical']
        target_ratio = target_w / target_h  # 9/16 = 0.5625
        
        # If already vertical or close, just resize
        current_ratio = w / h
        if current_ratio <= target_ratio * 1.1:
            return clip.resize(height=target_h)
        
        # Need to crop horizontal video to vertical
        # Calculate new width to match 9:16 ratio
        new_width = int(h * target_ratio)
        
        # Center crop (could be enhanced with face detection)
        x_center = w // 2
        x1 = max(0, x_center - new_width // 2)
        x2 = min(w, x1 + new_width)
        
        # Adjust if we hit edges
        if x2 - x1 < new_width:
            if x1 == 0:
                x2 = new_width
            else:
                x1 = w - new_width
        
        # Crop and resize
        cropped = clip.crop(x1=x1, x2=x2)
        return cropped.resize(height=target_h)
    
    def _smart_crop_square(self, clip):
        """
        Smart crop to 1:1 square format (1080x1080)
        """
        w, h = clip.size
        target_size = self.target_formats['square'][0]
        
        # Use the smaller dimension
        crop_size = min(w, h)
        
        # Center crop
        x_center = w // 2
        y_center = h // 2
        
        x1 = max(0, x_center - crop_size // 2)
        y1 = max(0, y_center - crop_size // 2)
        x2 = min(w, x1 + crop_size)
        y2 = min(h, y1 + crop_size)
        
        cropped = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        return cropped.resize((target_size, target_size))
    
    def _add_tiktok_subtitles(self, clip, text: str):
        """
        Add TikTok-style subtitles
        Large white text with black outline, centered
        """
        try:
            # Split text into chunks if too long
            max_chars_per_line = 30
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > max_chars_per_line:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(' '.join(current_line))
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            subtitle_text = '\n'.join(lines[:3])  # Max 3 lines
            
            # Create text clip
            txt_clip = TextClip(
                subtitle_text,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(clip.w * 0.9, None),
                align='center'
            )
            
            # Position at bottom (75% down)
            txt_clip = txt_clip.set_position(('center', 0.75), relative=True)
            txt_clip = txt_clip.set_duration(clip.duration)
            
            # Composite
            return CompositeVideoClip([clip, txt_clip])
            
        except Exception as e:
            print(f"⚠️ Subtitle error: {e}")
            return clip  # Return clip without subtitles if error
    
    def extract_multiple_clips(
        self,
        video_path: str,
        moments: List[Dict],
        output_dir: str,
        format_type: str = "vertical"
    ) -> List[str]:
        """
        Extract multiple clips from viral moments
        
        Args:
            video_path: Path to source video
            moments: List of moment dicts with start, end, text, hook
            output_dir: Directory for output clips
            format_type: Target format
            
        Returns:
            List of paths to generated clips
        """
        os.makedirs(output_dir, exist_ok=True)
        
        clips = []
        for i, moment in enumerate(moments, 1):
            output_path = os.path.join(output_dir, f"clip_{i:02d}.mp4")
            
            # Use hook as subtitle
            subtitle = moment.get('hook', moment.get('text', ''))[:100]
            
            clip_path = self.extract_clip(
                video_path=video_path,
                start=moment['start'],
                end=moment['end'],
                output_path=output_path,
                format_type=format_type,
                add_subtitles=True,
                subtitle_text=subtitle
            )
            
            if clip_path:
                clips.append(clip_path)
        
        print(f"✅ Extracted {len(clips)}/{len(moments)} clips")
        return clips


# Singleton instance
clip_extractor = ClipExtractor()
