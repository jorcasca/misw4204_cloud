from ..modelos import  db, Tareas
from .config import celery_app
import os
import zipfile
import py7zr
import tarfile
from ..__init__ import create_app

@celery_app.task(name='convert_file')
def convert_file(tarea_id):
    app = create_app('default')
    with app.app_context():
        tarea = Tareas.query.get(tarea_id)
        if tarea is None:
            return f'La tarea con id {tarea_id} no existe.'
        file_name = tarea.fileName
        new_format = tarea.newFormat
        if not os.path.exists('microservicio_auth/archivos/convertidos'):
            os.makedirs('microservicio_auth/archivos/convertidos')
        try:
            if new_format == 'ZIP':
                file_path = os.path.join('microservicio_auth/archivos/originales', file_name)
                zip_file_path = os.path.join('microservicio_auth/archivos/convertidos', file_name + '.zip')
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.write(file_path, file_name)
            elif new_format == '7Z':
                file_path = os.path.join('microservicio_auth/archivos/originales', file_name)
                seven_zip_file_path = os.path.join('microservicio_auth/archivos/convertidos', file_name + '.7z')
                with py7zr.SevenZipFile(seven_zip_file_path, 'w') as seven_zip_file:
                    seven_zip_file.write(file_path, file_name)
            elif new_format == 'TAR.GZ':
                file_path = os.path.join('microservicio_auth/archivos/originales', file_name)
                tar_gz_file_path = os.path.join('microservicio_auth/archivos/convertidos', file_name + '.tar.gz')
                with tarfile.open(tar_gz_file_path, 'w:gz') as tar_gz_file:
                    tar_gz_file.add(file_path, file_name)
            else:
                tarea.status = 'failed'
                db.session.commit()
                return {'message': tarea.mensaje}
            tarea.status = 'processed'
            db.session.commit()
            return f'La tarea con id {tarea_id} fue procesada.'
        except Exception as e:
            tarea.status = 'failed'
            db.session.commit()
            return f'La tarea con id {tarea_id} fue fallida.'
