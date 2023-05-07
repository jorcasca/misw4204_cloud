from ..modelos import  db, Tareas
from .config import celery_app
import os
import shutil
import zipfile
import py7zr
import tarfile
from ..__init__ import create_app
from google.cloud import storage

storage_client = storage.Client()
app = None
@celery_app.task(name='convert_file')
def convert_file(tarea_id):
    if app is None:
        app = create_app('default')
    with app.app_context():
        tarea = Tareas.query.get(tarea_id)
        if tarea is None:
            return f'La tarea con id {tarea_id} no existe.'
        file_name = tarea.fileName
        new_format = tarea.newFormat
        if not os.path.exists('microservicio_worker/archivos/convertidos'):
            os.makedirs('microservicio_worker/archivos/convertidos')
        if not os.path.exists('microservicio_worker/archivos/originales'):
            os.makedirs('microservicio_worker/archivos/originales')
        try:
            bucket_name = '<BUCKET_NAME>'
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob('archivos/originales/{}'.format(file_name))
            blob.download_to_filename('microservicio_worker/archivos/originales/{}'.format(file_name))
            if new_format == 'ZIP':
                file_path = os.path.join('microservicio_worker/archivos/originales', file_name)
                zip_file_path = os.path.join('microservicio_worker/archivos/convertidos', file_name + '.zip')
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.write(file_path, file_name)
                blob = bucket.blob('archivos/convertidos/{}.zip'.format(file_name))
                blob.upload_from_filename(zip_file_path)
            elif new_format == '7Z':
                file_path = os.path.join('microservicio_worker/archivos/originales', file_name)
                seven_zip_file_path = os.path.join('microservicio_worker/archivos/convertidos', file_name + '.7z')
                with py7zr.SevenZipFile(seven_zip_file_path, 'w') as seven_zip_file:
                    seven_zip_file.write(file_path, file_name)
                blob = bucket.blob('archivos/convertidos/{}.7z'.format(file_name))
                blob.upload_from_filename(seven_zip_file_path)
            elif new_format == 'TAR.GZ':
                file_path = os.path.join('microservicio_worker/archivos/originales', file_name)
                tar_gz_file_path = os.path.join('microservicio_worker/archivos/convertidos', file_name + '.tar.gz')
                with tarfile.open(tar_gz_file_path, 'w:gz') as tar_gz_file:
                    tar_gz_file.add(file_path, file_name)
                blob = bucket.blob('archivos/convertidos/{}.gz'.format(file_name))
                blob.upload_from_filename(seven_zip_file_path)
            else:
                tarea.status = 'failed'
                db.session.commit()
                return {'message': tarea.mensaje}
            shutil.rmtree('microservicio_worker/archivos')
            tarea.status = 'processed'
            db.session.commit()
            return f'La tarea con id {tarea_id} fue procesada.'
        except Exception as e:
            tarea.status = 'failed'
            db.session.commit()
            print(e)
            return f'La tarea con id {tarea_id} fue fallida.'
