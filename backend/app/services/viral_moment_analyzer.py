"""
Viral Moment Analyzer
Uses GPT-4 to identify viral moments in video transcripts
"""
import os
import json
import requests
from typing import List, Dict
from app.config import settings


class ViralMomentAnalyzer:
    """Analyzes transcripts to find viral TikTok/Shorts moments"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def analyze_transcript(
        self,
        segments: List[Dict],
        max_clips: int = 5,
        min_duration: int = 15,
        max_duration: int = 60
    ) -> List[Dict]:
        """
        Analyze transcript to find viral moments
        
        Args:
            segments: Transcript segments with timestamps
            max_clips: Maximum number of clips to generate
            min_duration: Minimum clip duration in seconds
            max_duration: Maximum clip duration in seconds
            
        Returns:
            [
                {
                    'start': 10.5,
                    'end': 40.2,
                    'score': 85,
                    'reason': 'Révélation surprenante',
                    'hook': 'Vous ne croirez jamais...',
                    'text': 'Full transcript of this moment'
                },
                ...
            ]
        """
        try:
            print(f"🧠 Analyzing transcript for viral moments...")
            
            # Format transcript with timestamps
            formatted_transcript = self._format_transcript(segments)
            
            # GPT-4 analysis
            prompt = f"""Analyse cette transcription de vidéo YouTube et identifie les {max_clips} moments les PLUS VIRAUX pour TikTok/Shorts.

CRITÈRES DE VIRALITÉ :
1. Phrases accrocheuses et captivantes
2. Révélations ou surprises
3. Conseils pratiques concrets
4. Moments émotionnels forts
5. Questions engageantes
6. Début percutant (hook fort)
7. Contenu qui donne envie de partager

CONTRAINTES :
- Durée : entre {min_duration} et {max_duration} secondes
- Chaque moment doit être autonome (compréhensible sans contexte)
- Privilégier les moments avec un début accrocheur

Pour chaque moment, fournis :
1. start: Timestamp de début (en secondes)
2. end: Timestamp de fin (en secondes)
3. score: Score viral de 0 à 100
4. reason: Pourquoi ce moment est viral (1 phrase)
5. hook: Phrase d'accroche pour attirer l'attention (max 10 mots)

TRANSCRIPTION :
{formatted_transcript}

Réponds UNIQUEMENT en JSON valide (array d'objets) :
[
  {{
    "start": 10.5,
    "end": 40.2,
    "score": 85,
    "reason": "Révélation surprenante sur un sujet tendance",
    "hook": "Vous ne croirez jamais ce secret..."
  }}
]
"""
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": "gpt-4-turbo-preview",
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un expert en contenu viral TikTok/Shorts. Tu identifies les moments les plus captivants dans les vidéos. Réponds UNIQUEMENT en JSON valide."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"❌ GPT-4 error: {response.status_code}")
                return []
            
            content = response.json()['choices'][0]['message']['content']
            
            # Extract JSON from response (handle markdown code blocks)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            moments = json.loads(content)
            
            # Add transcript text to each moment
            for moment in moments:
                moment['text'] = self._extract_text_for_moment(
                    segments,
                    moment['start'],
                    moment['end']
                )
            
            # Sort by score (highest first)
            moments.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            print(f"✅ Found {len(moments)} viral moments")
            for i, moment in enumerate(moments[:3], 1):
                print(f"   {i}. [{moment['start']:.1f}s-{moment['end']:.1f}s] Score: {moment['score']} - {moment['hook']}")
            
            return moments[:max_clips]
            
        except Exception as e:
            print(f"❌ Viral moment analysis error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _format_transcript(self, segments: List[Dict]) -> str:
        """Format transcript with timestamps for GPT-4"""
        lines = []
        for seg in segments:
            timestamp = f"[{seg['start']:.1f}s-{seg['end']:.1f}s]"
            lines.append(f"{timestamp} {seg['text']}")
        
        return '\n'.join(lines)
    
    def _extract_text_for_moment(
        self,
        segments: List[Dict],
        start: float,
        end: float
    ) -> str:
        """Extract transcript text for a specific time range"""
        texts = []
        for seg in segments:
            # Check if segment overlaps with moment
            if seg['start'] < end and seg['end'] > start:
                texts.append(seg['text'])
        
        return ' '.join(texts)


# Singleton instance
viral_moment_analyzer = ViralMomentAnalyzer()
