"""
Wav2Lip Service - Simplified version using modern libraries
Based on https://github.com/Rudrabha/Wav2Lip
"""
import os
import cv2
import numpy as np
import torch
from typing import Optional
import subprocess
import tempfile


class Wav2LipService:
    """
    Simplified Wav2Lip service for lip-sync video generation.
    Uses the Wav2Lip repository code with modern dependencies.
    """
    
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.wav2lip_path = os.path.join(os.path.dirname(__file__), 'Wav2Lip')
        self.checkpoint_path = os.path.join(self.wav2lip_path, 'checkpoints', 'wav2lip_gan.pth')
        
        print(f"Wav2Lip device: {self.device}")
        print(f"Wav2Lip path: {self.wav2lip_path}")
    
    def create_talking_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str = None
    ) -> Optional[str]:
        """
        Create a talking video from image and audio using Wav2Lip.
        
        Args:
            image_path: Path to avatar image
            audio_path: Path to audio file  
            output_path: Path for output video (optional)
            
        Returns:
            Path to generated video or None if failed
        """
        try:
            if output_path is None:
                output_path = tempfile.mktemp(suffix='.mp4')
            
            print(f"🎭 Wav2Lip: Creating talking video...")
            print(f"   Image: {image_path}")
            print(f"   Audio: {audio_path}")
            print(f"   Output: {output_path}")
            
            # Use Wav2Lip inference script
            cmd = [
                'python',
                os.path.join(self.wav2lip_path, 'inference.py'),
                '--checkpoint_path', self.checkpoint_path,
                '--face', image_path,
                '--audio', audio_path,
                '--outfile', output_path,
                '--resize_factor', '1',
                '--fps', '25'
            ]
            
            # Run Wav2Lip
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ Wav2Lip video generated: {output_path}")
                return output_path
            else:
                print(f"❌ Wav2Lip failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Wav2Lip exception: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def download_model(self):
        """
        Download Wav2Lip pre-trained model if not present.
        """
        checkpoint_dir = os.path.join(self.wav2lip_path, 'checkpoints')
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        if os.path.exists(self.checkpoint_path):
            print(f"✅ Wav2Lip model already downloaded")
            return True
        
        print(f"📥 Downloading Wav2Lip model...")
        
        # Try multiple sources
        sources = [
            "https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ",
            "https://github.com/Rudrabha/Wav2Lip/releases/download/models/wav2lip_gan.pth"
        ]
        
        for source in sources:
            try:
                import requests
                response = requests.get(source, stream=True, timeout=60)
                if response.status_code == 200:
                    with open(self.checkpoint_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Check if file is valid (should be ~150MB)
                    file_size = os.path.getsize(self.checkpoint_path)
                    if file_size > 100_000_000:  # > 100MB
                        print(f"✅ Model downloaded: {file_size / 1_000_000:.1f}MB")
                        return True
                    else:
                        os.remove(self.checkpoint_path)
                        print(f"⚠️ Downloaded file too small, trying next source...")
            except Exception as e:
                print(f"⚠️ Failed to download from {source[:50]}...: {e}")
                continue
        
        print(f"❌ Could not download Wav2Lip model from any source")
        return False


# Singleton instance
wav2lip_service = Wav2LipService()
