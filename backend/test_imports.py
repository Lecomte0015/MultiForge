#!/usr/bin/env python
import sys

print("=== Diagnostic Import Worker ===")
sys.stdout.flush()

try:
    print("1. Importing config...")
    sys.stdout.flush()
    from app.config import settings
    print("   ✅ Config OK")
    sys.stdout.flush()
except Exception as e:
    print(f"   ❌ Config FAILED: {e}")
    sys.exit(1)

try:
    print("2. Importing db_client...")
    sys.stdout.flush()
    from app.services.db_client import supabase_client
    print("   ✅ DB Client OK")
    sys.stdout.flush()
except Exception as e:
    print(f"   ❌ DB Client FAILED: {e}")
    sys.exit(1)

try:
    print("3. Importing video_editor...")
    sys.stdout.flush()
    from app.services.video_editor import combine_audio_video
    print("   ✅ Video Editor OK")
    sys.stdout.flush()
except Exception as e:
    print(f"   ❌ Video Editor FAILED: {e}")
    sys.exit(1)

try:
    print("4. Importing job_pipeline...")
    sys.stdout.flush()
    from app.workers.job_pipeline import run_pipeline
    print("   ✅ Pipeline OK")
    sys.stdout.flush()
except Exception as e:
    print(f"   ❌ Pipeline FAILED: {e}")
    sys.exit(1)

try:
    print("5. Importing celery_worker...")
    sys.stdout.flush()
    from app.workers.celery_worker import celery_app
    print("   ✅ Celery Worker OK")
    sys.stdout.flush()
except Exception as e:
    print(f"   ❌ Celery Worker FAILED: {e}")
    sys.exit(1)

print("\n=== Tous les imports OK! ===")
print("Le problème vient du démarrage de Celery lui-même, pas des imports.")
