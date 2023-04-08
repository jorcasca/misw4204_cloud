## 1. Crear entorno
Ejecutar:
`python3 -m venv venv`

## 2. Activar entorno
Ejecutar:
`source venv/bin/activate`

## 3. Instalar dependencias
Ejecutar:
`py -m pip install -r requirements.txt`

## 4. Ejecutar gestor de colas
En la ruta misw4204_cloud/Microservicios_Cloud, ejecutar:
`celery -A microservicio_auth.tareas worker -l info`

## 5. Ejecutar app
misw4204_cloud/Microservicios_Cloud/microservicio_auth, ejecutar:
`flask run`
