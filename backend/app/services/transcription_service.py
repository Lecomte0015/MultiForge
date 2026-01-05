"""
Transcription Service using OpenAI Whisper
Converts audio to text with timestamps
"""
import whisper
from typing import List, Dict, Optional
import os


class TranscriptionService:
    """Service for transcribing audio to text with timestamps"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize transcription service
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       base = good balance speed/quality
        """
        self.model_size = model_size
        self.model = None
        print(f"🎤 Whisper model: {model_size}")
    
    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self.model is None:
            print(f"📥 Loading Whisper model '{self.model_size}'...")
            self.model = whisper.load_model(self.model_size)
            print(f"✅ Whisper model loaded")
    
    def transcribe(self, audio_path: str) -> List[Dict]:
        """
        Transcribe audio file with word-level timestamps
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            [
                {
                    'start': 0.0,
                    'end': 5.2,
                    'text': 'Hello everyone, welcome to...',
                    'words': [
                        {'start': 0.0, 'end': 0.5, 'text': 'Hello'},
                        {'start': 0.6, 'end': 1.2, 'text': 'everyone'},
                        ...
                    ]
                },
                ...
            ]
        """
        try:
            if not os.path.exists(audio_path):
                print(f"❌ Audio file not found: {audio_path}")
                return []
            
            self.load_model()
            
            print(f"🎤 Transcribing audio: {audio_path}")
            
            # Transcribe with word timestamps
            result = self.model.transcribe(
                audio_path,
                word_timestamps=True,
                language='fr',  # Auto-detect or specify
                task='transcribe'
            )
            
            segments = []
            for segment in result['segments']:
                segment_data = {
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'words': []
                }
                
                # Extract word-level timestamps if available
                if 'words' in segment:
                    for word in segment['words']:
                        segment_data['words'].append({
                            'start': word.get('start', segment['start']),
                            'end': word.get('end', segment['end']),
                            'text': word.get('word', '').strip()
                        })
                
                segments.append(segment_data)
            
            print(f"✅ Transcription complete: {len(segments)} segments")
            return segments
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_full_text(self, segments: List[Dict]) -> str:
        """
        Get full transcript text from segments
        
        Args:
            segments: List of segment dictionaries
            
        Returns:
            Full transcript as string
        """
        return ' '.join([seg['text'] for seg in segments])
    
    def format_transcript_with_timestamps(self, segments: List[Dict]) -> str:
        """
        Format transcript with timestamps for GPT-4 analysis
        
        Args:
            segments: List of segment dictionaries
            
        Returns:
            Formatted transcript like:
            [0.0-5.2] Hello everyone, welcome to...
            [5.2-10.5] Today we're going to talk about...
        """
        lines = []
        for seg in segments:
            timestamp = f"[{seg['start']:.1f}-{seg['end']:.1f}]"
            lines.append(f"{timestamp} {seg['text']}")
        
        return '\n'.join(lines)


# Singleton instance
transcription_service = TranscriptionService(model_size="base")
