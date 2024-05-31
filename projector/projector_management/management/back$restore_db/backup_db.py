## author momo
import os
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

class Command(BaseCommand):
    help = 'Back up the database to a file'

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']
        backup_file = os.path.join(settings.BASE_DIR, f'{db_name}_backup.sql')

        if db_settings['ENGINE'] == 'django.db.backends.postgresql':
            command = f'PGPASSWORD={db_password} pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name} > {backup_file}'
        elif db_settings['ENGINE'] == 'django.db.backends.mysql':
            command = f'mysqldump -u {db_user} -p{db_password} -h {db_host} -P {db_port} {db_name} > {backup_file}'
        else:
            self.stdout.write(self.style.ERROR('Backup is only supported for PostgreSQL and MySQL databases'))
            return

        try:
            subprocess.run(command, shell=True, check=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully backed up the database to {backup_file}'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error during backup: {e}'))
