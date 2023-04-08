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
![image](https://user-images.githubusercontent.com/31069035/230703060-d8cfe9b7-a9dc-45ab-b0de-9415cdde068f.png)

## 5. Ejecutar app
misw4204_cloud/Microservicios_Cloud/microservicio_auth, ejecutar:
`flask run`
![image](https://user-images.githubusercontent.com/31069035/230703136-c29cdfb0-abcd-4241-be2b-c3aec9d69cfe.png)
