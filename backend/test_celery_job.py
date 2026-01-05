#!/usr/bin/env python
"""Test si on peut envoyer un job à Celery"""
from app.workers.celery_worker import process_video_job

print("Envoi d'un job de test...")
task = process_video_job.delay({"topic": "Test", "script": "Ceci est un test", "visual_style": "cinematic", "platform": "tiktok"})
print(f"✅ Job envoyé! ID: {task.id}")
print(f"Status: {task.status}")
