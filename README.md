# Requisitos

- VM en GCP (VM_WEB_BASE_SERVER)  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/e475d17e-59bd-49f5-b751-388383d519eb)

- VM en GCP (VM_WORKER_BASE_SERVER)  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/48f9e008-c356-4529-bfdd-9f41d0aabe4b)

- VM en GCP (VM_WEB_DISK)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/3c693b76-4a9a-4af7-bf89-6b493f0e6491)

- VM en GCP (VM_WORKER_DISK)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/9e403794-12ec-443a-8f77-fe5d4a5fffd7)

- VM en GCP (VM_WEB_IMAGE y VM_WORKER_IMAGE)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/ac0a4755-5057-40eb-a007-26dbec26c4ca)

- VM en GCP (VM_WEB_HEALTH_CHECK)  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/342d2389-c970-467d-9557-d3ab5c66fd67)

- VM en GCP (VM_WEB_INSTANCE_TEMPLATE)
![image](https://user-images.githubusercontent.com/31069035/236659004-b7276e9f-04d3-4da7-be7a-801563655c60.png)

- VM en GCP (VM_WEB_INSTANCE_GROUP y VM_WORKER_INSTANCE_GROUP)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/a3f47cc4-3a9c-496f-8439-907a6ad0eace)

- VM en GCP (VM_WEB_LOAD_BALANCER_SERVER)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/fbe01bef-1791-4897-9d5c-29d6c994af69)

- Bucket en GCP (BUCKET)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/59f8a4b1-b183-4765-867c-47c0ee570e99)

- VM en GCP (PUB/SUB)  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/5a86be38-0c55-4795-85fa-c88a4059f6b2)

- Cloud SQL en GCP (POSTGRES_SERVER)  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/d016ce56-4698-4533-8792-840de282b84c)


Nota: La configuración de los puertos de IPs de las instancias (como 80 para WEB_SERVER y WORKER_SERVER, 5432 para POSTGRES_SERVER) deben estar establecidas en las reglas de firewall de GCP y reglas de conexión en caso de Cloud SQL.
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/b3e76e06-8650-43b8-85af-eac023107e47)

# 1. Configurar POSTGRES_SERVER

**1.1**  Por defecto, al crear una instancia Cloud SQL postgress, esta ya viene configurada con el usuario postgres.  
**1.2** Configurar la contraseña del usuario como "contrasena123", ignorar paso si la contraseña fue configurada en la creación de la instancia.
```bash
ALTER USER postgres WITH PASSWORD 'contrasena123';
```
**1.3** Crear la base de datos "baseapp" , ignorar paso si la bd fue configurada en la creación de la instancia.
```bash
createdb baseapp
```  
**1.4** En las reglas de conexión de la instancia es importante agregar las IPs de los servers WEB_SERVER, WORKER_SERVER y NFS_SERVER. De esta manera, aseguramos que estas instancias puedan acceder a la base de datos.

# 2. Configurar BUCKET

**2.1**  Cree un Bucket con GCP Cloud Storage, no olvide que debe crear credenciales de cuenta con rol de administración de storage para que las maquinas WEB_API y WORKER puedan acceder al Bucket. 
![image](https://user-images.githubusercontent.com/31069035/236659184-50b5f7f8-26d0-439c-9813-d609483526c6.png)

# 3. Configurar PUB/SUB
**3.1**  Cree un Topic y su correspondiente Suscripción con GCP Pub/Sub, no olvide que debe crear credenciales de cuenta con rol de administración de Pub/Sub para que las maquinas WEB_API y WORKER puedan acceder al servicio. 
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/cc170762-2d0a-4d6c-be2b-40790b2a5385)

# 4. Configurar WORKER_SERVER

**4.1** Clonar el presente proyecto.  
**4.2** Ingresar al proyecto clonado y crear un entorno de desarrollo en la ruta misw4204_cloud.  
`python3 -m venv venv`  
**4.3** Activar entorno.  
`source venv/bin/activate`  
**4.4** Instalar dependencias de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker.  
`python3 -m pip install -r requirements.txt`  
**4.5** En el archivo app.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker, modificar la dirección del POSTGRES_SERVER.
```bash
engine = create_engine('postgresql://postgres:contrasena123@<POSTGRES_SERVER_IP>/baseapp')
```  
**4.6** En el archivo app.py de la ruta misw4204_cloud\Microservicios_Cloud\microservicio_worker, modificar el nombre del BUCKET_NAME con el nombre del bucket creado en Cloud Storage, PROJECT_ID con el id del proyecto de GCP y SUB_NAME con el nombre de la subscripción en PUB/SUB.  
```bash
project_id = "<PROJECT_ID>"
subscription_name = "<SUB_NAME>"
bucket_name = '<BUCKET_NAME>'
```  
**4.7** En el archivo run_worker.service, actualice PATH_TO_PROJECT con la ruta del proyecto misw4204_cloud y MACHINE_USER con el usuario de la maquina.  
```bash
User=<MACHINE_USER>
WorkingDirectory=<PATH_TO_PROJECT>/misw4204_cloud
ExecStart=<PATH_TO_PROJECT>/misw4204_cloud/Microservicios_Cloud/microservicio_worker/run_worker.sh
``` 
NOTA: Ejecutar para darle permisos de ejecución.  
**4.8** En el archivo run_worker.sh, actualice GOOGLE_CREDENTIALS_PATH con las credenciales de Google para acceder al servicio como se mencionó en el punto 2.  
```bash
export GOOGLE_APPLICATION_CREDENTIALS="<GOOGLE_CREDENTIALS_PATH>"
``` 
NOTA: Ejecutar para darle permisos de ejecución.  
```  
sudo chmod +x run_worker.sh  
```  
**4.9** Ubique el archivo run_worker.service en /etc/systemd/system/ para arrancar los servicios.  
**4.10** Debe activar los servicios con los siguientes comandos: 
```bash
sudo systemctl start run_worker.service
sudo systemctl enable run_worker.service
```  

# 5. Configurar WEB_SERVER

**5.1** Clonar el presente proyecto.  
**5.2** Ingresar al proyecto clonado y crear un entorno de desarrollo.  
`python3 -m venv venv`  
**5.3** Activar entorno.  
`source venv/bin/activate`  
**5.4** Instalar dependencias.  
`python3 -m pip install -r requirements.txt`  
**5.5** En el archivo __init__.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth, modificar la dirección del POSTGRES_SERVER.
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://baseapp:contrasena123@<POSTGRES_SERVER_IP>/baseapp'
```
**5.6** En el archivo vistas.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth, modificar BUCKET_NAME con el nombre del bucket creado en Cloud Storage, PROJECT_ID con el id del proyecto de GCP y TOPIC_NAME con el nombre del topic en PUB/SUB.  
```bash
project_id = "<PROJECT_ID>"
topic_name = "<TOPIC_NAME>"
bucket_name = '<BUCKET_NAME>'
```  
**5.7** Ejecutar app del WEB_SERVER en la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker.  
`flask run`  
**5.8** Una vez confirme todo corre perfectamente, baje esos servicios CTRL+C.  
**5.9** En el archivo run_gunicorn.sh, actualice GOOGLE_CREDENTIALS_PATH con las credenciales de Google para acceder al servicio como se mencionó en el punto 2.  
NOTA: Ejecutar para darle permisos de ejecución.  
```  
sudo chmod +x run_gunicorn.sh  
```  
**5.10** En el archivo run_gunicorn.service, actualice PATH_TO_PROJECT con la ruta del proyecto misw4204_cloud y MACHINE_USER con el usuario de la maquina.  
NOTA: Ejecutar para darle permisos de ejecución.  
```bash
User=<MACHINE_USER>
WorkingDirectory=<PATH_TO_PROJECT>/misw4204_cloud
ExecStart=<PATH_TO_PROJECT>/misw4204_cloud/Microservicios_Cloud/microservicio_auth/run_gunicorn.sh
``` 
**5.11** Ubique el archivo run_gunicorn.service en /etc/systemd/system/ para arrancar los servicios.  
**5.12** Debe activar los servicios con los siguientes comandos: 
```bash
sudo systemctl start run_gunicorn.service
sudo systemctl enable run_gunicorn.service
```  
**5.13** Mueva el archivo microservicio_auth_site a /etc/nginx/sites-avaliable de esta manera se mapeara el servicio de gunicorn que esta por defecto en 8000 por medio de nginx escuhando por el 80.  
NOTA: Es importante que el servicio NGINX se active por lo que es posible deba seguir este tutoria:
[Tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)  
NOTA: por defecto NGINX crea un site default en /etc/nginx/sites-avaliable, es importante que cambie el puerto de escucha por defecto de ese site de 80 a otro puerto, de lo contrario tendrá conflictos al ejecutar
sudo nginx -t  
# 6. Evidencia
Load balancer respondiendo correctamente:  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/310fe658-b225-4f30-9a6b-435284b39c0d)

Load balancer
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/45ae1195-5b04-46bb-b2e9-b933be222bcd)

Grupo de instancias corriendo:  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/5b0e8e01-6255-4f34-b965-213897385be5)

Salud de las instancias desde el grupo:  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/5e88db84-3e97-4b48-96fd-ab668aa4797f)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/1dc4dd78-97be-4e85-b9df-7a0c52076d56)

