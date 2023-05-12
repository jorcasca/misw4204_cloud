# Requisitos

- VM en GCP (VM_WEB_BASE_SERVER)  
![image](https://user-images.githubusercontent.com/31069035/236658969-0e654b73-f861-4533-affc-5160c18bbab1.png)

- VM en GCP (VM_WEB_DISK)
![image](https://user-images.githubusercontent.com/31069035/236658979-8d47af8d-5b0a-408e-8688-9cb351777318.png)

- VM en GCP (VM_WEB_IMAGE)
![image](https://user-images.githubusercontent.com/31069035/236658988-011b1a20-d971-43f8-a0af-190d814574cd.png)

- VM en GCP (VM_WEB_HEALTH_CHECK)  
![image](https://user-images.githubusercontent.com/31069035/236658995-320a5c5a-ea19-46a3-bf91-fe6d0e8c10ce.png)

- VM en GCP (VM_WEB_INSTANCE_TEMPLATE)
![image](https://user-images.githubusercontent.com/31069035/236659004-b7276e9f-04d3-4da7-be7a-801563655c60.png)

- VM en GCP (VM_WEB_INSTANCE_GROUP)
![image](https://user-images.githubusercontent.com/31069035/236659014-def5af8b-6fce-4104-b36c-6a4a64ec24ed.png)

- VM en GCP (VM_WEB_LOAD_BALANCER_SERVER)
![image](https://user-images.githubusercontent.com/31069035/236659026-8780c2d2-b49b-46da-8de0-73b201cd5de9.png)

- Bucket en GCP (BUCKET)
![image](https://user-images.githubusercontent.com/31069035/236659042-ca878da0-9fe3-40b2-99d0-abc0a95758d6.png)

- VM en GCP (WORKER_SERVER)  
![image](https://user-images.githubusercontent.com/31069035/236659057-762e9e9e-ada5-45da-9b65-62de8d311e31.png)

- Cloud SQL en GCP (POSTGRES_SERVER)  
![image](https://user-images.githubusercontent.com/31069035/236659066-43bed0b2-634c-4df7-abf2-47fb5fde2d14.png)


Nota: La configuración de los puertos de IPs de las instancias (como 80 para WEB_SERVER y WORKER_SERVER, 5432 para POSTGRES_SERVER) deben estar establecidas en las reglas de firewall de GCP y reglas de conexión en caso de Cloud SQL.
![image](https://user-images.githubusercontent.com/31069035/233866267-7410873d-a5db-4bd1-bc24-c2435c5b0389.png)


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

# 3. Configurar WORKER_SERVER

**3.1** Clonar el presente proyecto.  
**3.2** Ingresar al proyecto clonado y crear un entorno de desarrollo en la ruta misw4204_cloud.  
`python3 -m venv venv`  
**3.3** Activar entorno.  
`source venv/bin/activate`  
**3.4** Instalar dependencias de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker.  
`python3 -m pip install -r requirements.txt`  
**3.5** En el archivo app.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker, modificar la dirección del POSTGRES_SERVER.
```bash
engine = create_engine('postgresql://postgres:contrasena123@<POSTGRES_SERVER_IP>/baseapp')
```  
**3.6** En el archivo app.py de la ruta misw4204_cloud\Microservicios_Cloud\microservicio_worker, modificar el nombre del BUCKET_NAME con el nombre del bucket creado en Cloud Storage, PROJECT_ID con el id del proyecto de GCP y SUB_NAME con el nombre de la subscripción en PUB/SUB.  
**3.7** En el archivo run_worker.service, actualice PATH_TO_PROJECT con la ruta del proyecto misw4204_cloud y MACHINE_USER con el usuario de la maquina.  
NOTA: Ejecutar para darle permisos de ejecución.  
**3.8** En el archivo run_worker.sh, actualice GOOGLE_CREDENTIALS_PATH con las credenciales de Google para acceder al servicio como se mencionó en el punto 2.  
NOTA: Ejecutar para darle permisos de ejecución.  
```  
sudo chmod +x run_worker.sh  
```  
**3.9** Ubique el archivo run_worker.service en /etc/systemd/system/ para arrancar los servicios.  
**3.10** Debe activar los servicios con los siguientes comandos: 
```bash
sudo systemctl start run_worker.service
sudo systemctl enable run_worker.service
```  

# 4. Configurar WEB_SERVER

**4.1** Clonar el presente proyecto.  
**4.2** Ingresar al proyecto clonado y crear un entorno de desarrollo.  
`python3 -m venv venv`  
**4.3** Activar entorno.  
`source venv/bin/activate`  
**4.4** Instalar dependencias.  
`python3 -m pip install -r requirements.txt`  
**4.5** En el archivo __init__.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth, modificar la dirección del POSTGRES_SERVER.
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://baseapp:contrasena123@<POSTGRES_SERVER_IP>/baseapp'
```
**4.6** En el archivo vistas.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth, modificar BUCKET_NAME con el nombre del bucket creado en Cloud Storage, PROJECT_ID con el id del proyecto de GCP y TOPIC_NAME con el nombre del topic en PUB/SUB.  
**4.7** Ejecutar app del WEB_SERVER en la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker.  
`flask run`  
**4.8** Una vez confirme todo corre perfectamente, baje esos servicios CTRL+C.  
**4.9** En el archivo run_gunicorn.sh, actualice GOOGLE_CREDENTIALS_PATH con las credenciales de Google para acceder al servicio como se mencionó en el punto 2.  
NOTA: Ejecutar para darle permisos de ejecución.  
```  
sudo chmod +x run_gunicorn.sh  
```  
**4.10** En el archivo run_gunicorn.service, actualice PATH_TO_PROJECT con la ruta del proyecto misw4204_cloud y MACHINE_USER con el usuario de la maquina.  
NOTA: Ejecutar para darle permisos de ejecución.  
**4.11** Ubique el archivo run_gunicorn.service en /etc/systemd/system/ para arrancar los servicios.  
**4.12** Debe activar los servicios con los siguientes comandos: 
```bash
sudo systemctl start run_gunicorn.service
sudo systemctl enable run_gunicorn.service
```  
**4.13** Mueva el archivo microservicio_auth_site a /etc/nginx/sites-avaliable de esta manera se mapeara el servicio de gunicorn que esta por defecto en 8000 por medio de nginx escuhando por el 80.  

NOTA: Es importante que el servicio NGINX se active por lo que es posible deba seguir este tutoria:
[Tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)  
NOTA: por defecto NGINX crea un site default en /etc/nginx/sites-avaliable, es importante que cambie el puerto de escucha por defecto de ese site de 80 a otro puerto, de lo contrario tendrá conflictos al ejecutar
sudo nginx -t  
# 5. Evidencia
Load balancer respondiendo correctamente:  
![image](https://user-images.githubusercontent.com/31069035/236659966-343fbaf1-785e-402e-ba19-f9abb4ffb448.png)

Grupo de instancias corriendo:  
![image](https://user-images.githubusercontent.com/31069035/236659999-78afb7e3-13e1-4408-8a14-60820b7fd5b2.png)

Salud de las instancias desde el grupo:  
![image](https://user-images.githubusercontent.com/31069035/236660016-21bc957c-5693-4378-a764-de5ade339d90.png)
