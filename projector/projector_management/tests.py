from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Projector, Booking

class ProjectorTests(TestCase):

    def setUp(self):
        # Set up the test client
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.projector = Projector.objects.create(
            name='Test Projector',
            description='A test projector',
            quantity=5,
            model_type='Test Model',
            serial_number='12345ABC'
        )

    def test_book_projector_get(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')

        # Test GET request to book_projector endpoint
        response = self.client.get(reverse('book_projector'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request/book_projector.html')

    def test_book_projector_post(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')

        # Test POST request to book_projector endpoint
        data = {
            'projector': self.projector.id,
            'booking_date': '2024-06-01',
            'start_time': '2024-06-01T10:00:00Z',
            'end_time': '2024-06-01T12:00:00Z'
        }
        response = self.client.post(reverse('book_projector'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        self.assertRedirects(response, reverse('user_dashboard'))

    def test_validate_booking(self):
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            projector=self.projector,
            booking_date='2024-06-01',
            start_time='2024-06-01T10:00:00Z',
            end_time='2024-06-01T12:00:00Z',
            status='Pending'
        )

        # Log in the superuser
        admin_user = User.objects.create_superuser(username='admin', password='admin12345')
        self.client.login(username='admin', password='admin12345')

        # Test GET request to validate_booking endpoint
        response = self.client.get(reverse('validate_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request/validate_booking.html')

        # Test POST request to approve the booking
        response = self.client.post(reverse('validate_booking', args=[booking.id]), {'action': 'approve'})
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Approved')

    def test_admin_dashboard(self):
        # Log in the superuser
        admin_user = User.objects.create_superuser(username='admin', password='admin12345')
        self.client.login(username='admin', password='admin12345')

        # Test GET request to admin_dashboard endpoint
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/admin_dashboard.html')
