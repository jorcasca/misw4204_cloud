from google.cloud import storage
from google.cloud import pubsub_v1
import os
import shutil
import zipfile
import py7zr
import tarfile
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql://postgres:contrasena123@<POSTGRES_SERVER_IP>/baseapp')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

project_id = "<PROJECT_ID>"
subscription_name = "<SUB_NAME>"
storage_client = storage.Client()
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

class Tareas(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    timeStamp = Column(DateTime, default=datetime.datetime.utcnow)
    fileName = Column(String(500))
    newFormat = Column(String(100))
    status = Column(String(50))
    usuario = Column(Integer, ForeignKey('usuario.id'))
    
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100)) 
    email = Column(String(100), unique=True)

def callback(message):
    tarea_id = message.data.decode("utf-8")
    message.ack()
    
    print(f'START PROCESING... task with id {tarea_id}')
    tarea = session.get(Tareas, tarea_id)
    if tarea is None:
        return
    file_name = tarea.fileName
    new_format = tarea.newFormat
    if not os.path.exists('microservicio_worker/archivos/convertidos'):
        os.makedirs('microservicio_worker/archivos/convertidos')
    if not os.path.exists('microservicio_worker/archivos/originales'):
        os.makedirs('microservicio_worker/archivos/originales')
        
    try:
        print(f'DOWNLOADING... {file_name} from bucket')
        bucket_name = '<BUCKET_NAME>'
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob('archivos/originales/{}'.format(file_name))
        blob.download_to_filename('microservicio_worker/archivos/originales/{}'.format(file_name))
        if new_format == 'ZIP':
            print(f'COMPRESSING... {file_name} to zip')
            file_path = os.path.join('microservicio_worker/archivos/originales', file_name)
            zip_file_path = os.path.join('microservicio_worker/archivos/convertidos', file_name + '.zip')
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(file_path, file_name)
            blob = bucket.blob(f'archivos/convertidos/{file_name}.zip')
            print(f'UPLOADING... {file_name}.zip to bucket') 
            blob.upload_from_filename(zip_file_path)
        elif new_format == '7Z':
            print(f'COMPRESSING... {file_name} to 7z')
            file_path = os.path.join('microservicio_worker/archivos/originales', file_name)
            seven_zip_file_path = os.path.join('microservicio_worker/archivos/convertidos', file_name + '.7z')
            with py7zr.SevenZipFile(seven_zip_file_path, 'w') as seven_zip_file:
                seven_zip_file.write(file_path, file_name)
            print(f'UPLOADING... {file_name}.7z to bucket')    
            blob = bucket.blob(f'archivos/convertidos/{file_name}.7z')
            blob.upload_from_filename(seven_zip_file_path)
        elif new_format == 'TAR.GZ':
            print(f'COMPRESSING... {file_name} to tar.gz')
            file_path = os.path.join('microservicio_worker/archivos/originales', file_name)
            tar_gz_file_path = os.path.join('microservicio_worker/archivos/convertidos', file_name + '.tar.gz')
            with tarfile.open(tar_gz_file_path, 'w:gz') as tar_gz_file:
                tar_gz_file.add(file_path, file_name)
            print(f'UPLOADING... {file_name}.tar.gz to bucket') 
            blob = bucket.blob(f'archivos/convertidos/{file_name}.tar.gz')
            blob.upload_from_filename(seven_zip_file_path)
        else:
            tarea.status = 'failed'
            session.commit()
        shutil.rmtree('microservicio_worker/archivos')
        tarea.status = 'processed'
        session.commit()
        print(f'FINISH PROCESING... task with id {tarea_id}')
        print('--------------------o----------------------')
    except Exception as e:
        tarea.status = 'failed'
        session.commit()
        print(e)

subscriber.subscribe(subscription_path, callback=callback)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print('Servicio iniciado, esperando mensajes...')
    while True:
        pass
