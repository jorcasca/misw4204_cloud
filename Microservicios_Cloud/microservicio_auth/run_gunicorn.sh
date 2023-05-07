#!/bin/bash
source venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS="<GOOGLE_CREDENTIALS_PATH>"
cd ./Microservicios_Cloud
gunicorn microservicio_auth.app:app -w 4 --access-logfile - --error-logfile - --log-level info