# Requisitos

- VM en GCP (WEB_SERVER)
- VM en GCP (WORKER_SERVER)
- VM en GCP (NFS_SERVER)
- Cloud SQL en GCP (POSTGRES_SERVER)
![image](https://user-images.githubusercontent.com/31069035/233821353-10f023fc-3957-467c-be3e-3dc5df888697.png)
![image](https://user-images.githubusercontent.com/31069035/233821390-8642ba92-507e-43d9-81d7-7817c638b557.png)

Nota: La configuración de los puertos de IPs de las instancias (como 5000 para WEB_SERVER y WORKER_SERVER, 5432 para POSTGRES_SERVER y 2049 para NFS_SERVER) deben estar establecidas en las reglas de firewall de GCP y reglas de conexión en caso de Cloud SQL.
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

# 2. Configurar NFS_SERVER

**2.1**  Configurar una carpeta compartida para posteriormente ser montada en los clientes WEB_SERVER y WORKER_SERVER. Para este caso, la carpeta debe ser creada en el directorio /var/nfs/archivos.
[Haga clic aquí para ver tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)

# 3. Configurar WORKER_SERVER

**3.1** Clonar el presente proyecto.
**3.2** Montar la carpeta /nfs/archivos/ y contectarla al NFS_SERVER siguiendo la sesión de cliente del anterior tutorial.
[Haga clic aquí para ver tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04#step-5-creating-mount-points-and-mounting-directories-on-the-client)  
**3.3** Ingresar al proyecto clonado y crear un entorno de desarrollo.  
`python3 -m venv venv`  
**3.4** Activar entorno.  
`source venv/bin/activate`  
**3.5** Instalar dependencias.  
`py -m pip install -r requirements.txt`  
**3.6** En el archivo __init__.py de la ruta  misw4204_cloud/Microservicios_Cloud/microservicio_worker, modificar la dirección del POSTGRES_SERVER.
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://baseapp:contrasena123@<POSTGRES_SERVER_IP>/baseapp'
```
**3.7** Ejecutar gestor de colas ejecutando el siguiente comando en la ruta misw4204_cloud/Microservicios_Cloud.  
`celery -A microservicio_worker.tareas worker -l info`  
**3.8** Ejecutar app del WORKER_SERVER en la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker.  
`flask run`  

# 4. Configurar WEB_SERVER

**4.1** Clonar el presente proyecto.
**4.2** Montar la carpeta /nfs/archivos/ y contectarla al NFS_SERVER siguiendo la sesión de cliente del anterior tutorial.
[Haga clic aquí para ver tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04#step-5-creating-mount-points-and-mounting-directories-on-the-client)  
**4.3** Ingresar al proyecto clonado y crear un entorno de desarrollo.  
`python3 -m venv venv`  
**4.4** Activar entorno.  
`source venv/bin/activate`  
**4.5** Instalar dependencias.  
`py -m pip install -r requirements.txt`  
**4.6** En el archivo __init__.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth, modificar la dirección del POSTGRES_SERVER.
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://baseapp:contrasena123@<POSTGRES_SERVER_IP>/baseapp'
```
**4.7** En el archivo vistas.py de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth, modificar la dirección del WORKER_SERVER.
```bash
requests.get("<WORKER_SERVER_IP>:5000/api/tasks/{}".format(nueva_tarea.id)) # Linea 111
```
**4.8** Ejecutar app del WEB_SERVER en la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker.  
`flask run`  

# 5. Evidencia
![image](https://user-images.githubusercontent.com/31069035/233821446-acebafa3-7933-4e2c-85fe-1fa708df58ca.png)
