# Requisitos

- App Engine en GCP (WEB_SERVER y WORKER_SERVER)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/fbe01bef-1791-4897-9d5c-29d6c994af69)

- Bucket en GCP (BUCKET)
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/59f8a4b1-b183-4765-867c-47c0ee570e99)

- Message Service en GCP (PUB/SUB)  
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
**1.4** En las reglas de conexión de la instancia es importante agregar las IPs o su rango de las instancias WEB_SERVER y WORKER_SERVER. De esta manera, aseguramos que estas instancias puedan acceder a la base de datos.

# 2. Configurar BUCKET

**2.1**  Cree un Bucket con GCP Cloud Storage, no olvide que debe crear credenciales de cuenta con rol de administración de storage para que las instancias WEB_API y WORKER puedan acceder al Bucket. 
![image](https://user-images.githubusercontent.com/31069035/236659184-50b5f7f8-26d0-439c-9813-d609483526c6.png)

# 3. Configurar PUB/SUB
**3.1**  Cree un Topic y su correspondiente Suscripción con GCP Pub/Sub, no olvide que debe crear credenciales de cuenta con rol de administración de Pub/Sub para que las instancias WEB_API y WORKER puedan acceder al servicio. 
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/cc170762-2d0a-4d6c-be2b-40790b2a5385)

# 4. Configurar WORKER_SERVER

**4.1** Clonar el presente proyecto en la consola GCP de su proyecto cloud.  
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
**4.7** Actualice GOOGLE_CREDENTIALS_PATH con las credenciales de Google para acceder al servicio como se mencionó en el punto 2.  
```bash
export GOOGLE_APPLICATION_CREDENTIALS="<GOOGLE_CREDENTIALS_PATH>"
``` 
NOTA: Recomendamos que ubique el archivo de credenciales .json dentro de la carpeta misw4204_cloud.  
**4.9** Debe activar el servicio en App Engine, para ello vaya a la ruta misw4204_cloud/Microservicios_Cloud/microservicio_worker y ejecute los siguientes comandos: 
```bash
gcloud app create
gcloud app deploy
```  
**4.9** Al finalizar, asegurese que el servicio este corriendo:  
```bash
gcloud app browse
```  

# 5. Configurar WEB_SERVER

**5.1** Clonar el presente proyecto en la consola GCP de su proyecto cloud. Puede trabajar en el mismo proyecto clonado en el paso 4 (Configurar WORKER_SERVER).  
**5.2** Ingresar al proyecto clonado y crear un entorno de desarrollo en la ruta misw4204_cloud. Ignorar este paso si ya se creó el entorno.  
`python3 -m venv venv`  
**5.3** Activar entorno.  
`source venv/bin/activate`  
**5.4** Instalar dependencias de la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth.  
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
**5.7** Actualice GOOGLE_CREDENTIALS_PATH con las credenciales de Google para acceder al servicio como se mencionó en el punto 2. Ignorar este paso si ya se actualizo la variable.  
```bash
export GOOGLE_APPLICATION_CREDENTIALS="<GOOGLE_CREDENTIALS_PATH>"
``` 
NOTA: Recomendamos que ubique el archivo de credenciales .json dentro de la carpeta misw4204_cloud.  
**5.8** Debe activar el servicio en App Engine, para ello vaya a la ruta misw4204_cloud/Microservicios_Cloud/microservicio_auth y ejecute los siguientes comandos: 
```bash
gcloud app create
gcloud app deploy
```  
**5.9** Al finalizar, asegurese que el servicio este corriendo:  
```bash
gcloud app browse
```  

# 6. Evidencia
Servicios en App Engine respondiendo correctamente:  
![image](https://github.com/jorcasca/misw4204_cloud/assets/31069035/310fe658-b225-4f30-9a6b-435284b39c0d)
