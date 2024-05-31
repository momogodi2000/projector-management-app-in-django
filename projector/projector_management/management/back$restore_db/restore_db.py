## author momo
import os
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

class Command(BaseCommand):
    help = 'Restore the database from a backup file'

    def add_arguments(self, parser):
        parser.add_argument('backup_file', type=str, help='The backup file to restore from')

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']
        backup_file = kwargs['backup_file']

        if db_settings['ENGINE'] == 'django.db.backends.postgresql':
            command = f'PGPASSWORD={db_password} psql -U {db_user} -h {db_host} -p {db_port} {db_name} < {backup_file}'
        elif db_settings['ENGINE'] == 'django.db.backends.mysql':
            command = f'mysql -u {db_user} -p{db_password} -h {db_host} -P {db_port} {db_name} < {backup_file}'
        else:
            self.stdout.write(self.style.ERROR('Restore is only supported for PostgreSQL and MySQL databases'))
            return

        try:
            subprocess.run(command, shell=True, check=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully restored the database from {backup_file}'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error during restore: {e}'))
