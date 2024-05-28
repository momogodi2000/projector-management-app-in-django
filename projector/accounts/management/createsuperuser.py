from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='prince').exists():
            User.objects.create_superuser('prince', 'prince@gmail.com', 'password')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser prince'))
        else:
            self.stdout.write(self.style.WARNING('Superuser prince already exists'))
