#!/bin/bash
source venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS="<GOOGLE_CREDENTIALS_PATH>"
cd ./Microservicios_Cloud
celery -A microservicio_worker.tareas worker -l info