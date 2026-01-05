from celery import Celery, current_task
from app.config import settings
from app.workers.job_pipeline import run_pipeline
import time

# Configuration de Celery
celery_app = Celery(
    "multiforge_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(bind=True)
def process_video_job(self, request_data: dict):
    """
    Wrapper de tâche Celery qui appelle le pipeline métier.
    Met à jour l'état pour le frontend.
    """
    def update_progress(progress, step, logs):
        self.update_state(
            state='PROGRESS',
            meta={
                'progress': progress,
                'current_step': step,
                'logs': logs
            }
        )

    # Lancement du pipeline
    try:
        result = run_pipeline(request_data, update_progress)
        return result
    except Exception as e:
        # En prod, logger l'erreur ici
        raise e