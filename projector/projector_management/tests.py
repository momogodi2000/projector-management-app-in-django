from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Projector, Booking, Withdrawal, Deposit, Device

class ProjectorTests(TestCase):

    def setUp(self):
        # Set up the test client
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin12345')
        self.device = Device.objects.create(name='HDMI Cable', description='An HDMI cable')
        self.projector = Projector.objects.create(
            name='Test Projector',
            description='A test projector',
            quantity=5,
            model_type='Test Model',
            serial_number='12345ABC'
        )
        self.booking = Booking.objects.create(
            user=self.user,
            projector=self.projector,
            booking_date='2024-06-01',
            start_time='2024-06-01T10:00:00Z',
            end_time='2024-06-01T12:00:00Z',
            status='Pending'
        )
        self.withdrawal = Withdrawal.objects.create(
            user=self.user,
            projector=self.projector
        )
        self.withdrawal.devices.add(self.device)

    def test_book_projector_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('book_projector'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request/book_projector.html')

    def test_book_projector_post(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'projector': self.projector.id,
            'booking_date': '2024-06-01',
            'start_time': '2024-06-01T10:00:00Z',
            'end_time': '2024-06-01T12:00:00Z'
        }
        response = self.client.post(reverse('book_projector'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_dashboard'))

    def test_validate_booking_get(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.get(reverse('validate_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request/validate_booking.html')

    def test_validate_booking_post_approve(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.post(reverse('validate_booking', args=[self.booking.id]), {'action': 'approve'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'Approved')

    def test_validate_booking_post_reject(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.post(reverse('validate_booking', args=[self.booking.id]), {'action': 'reject'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'Rejected')

    def test_admin_dashboard(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/admin_dashboard.html')

    def test_withdraw_projector(self):
        self.client.login(username='admin', password='admin12345')
        data = {
            'user': self.user.id,
            'projector': self.projector.id,
            'devices': [self.device.id]
        }
        response = self.client.post(reverse('withdraw_projector'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard'))
        withdrawal = Withdrawal.objects.last()
        self.assertEqual(withdrawal.user, self.user)
        self.assertEqual(withdrawal.projector, self.projector)
        self.assertIn(self.device, withdrawal.devices.all())

    def test_deposit_projector(self):
        self.client.login(username='admin', password='admin12345')
        data = {
            'withdrawal': self.withdrawal.id,
            'returned_devices': [self.device.id]
        }
        response = self.client.post(reverse('deposit_projector'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard'))
        deposit = Deposit.objects.last()
        self.assertEqual(deposit.withdrawal, self.withdrawal)
        self.assertIn(self.device, deposit.returned_devices.all())

    def test_manage_projectors_get(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.get(reverse('manage_projectors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/manage_projectors.html')

    def test_manage_projectors_post(self):
        self.client.login(username='admin', password='admin12345')
        data = {
            'name': 'New Projector',
            'description': 'A new projector description',
            'quantity': 10,
            'model_type': 'New Model',
            'serial_number': 'NEW12345'
        }
        response = self.client.post(reverse('manage_projectors'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_projectors'))
        projector = Projector.objects.get(serial_number='NEW12345')
        self.assertEqual(projector.name, 'New Projector')
        self.assertEqual(projector.description, 'A new projector description')

    def test_manage_users_get(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/manage_users.html')

    def test_delete_projector(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.post(reverse('delete_projector', args=[self.projector.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_projectors'))
        with self.assertRaises(Projector.DoesNotExist):
            Projector.objects.get(id=self.projector.id)

    def test_update_projector(self):
        self.client.login(username='admin', password='admin12345')
        data = {
            'name': 'Updated Projector',
            'description': 'Updated description',
            'quantity': 8,
            'model_type': 'Updated Model',
            'serial_number': '12345ABC'  # Use the same serial number
        }
        response = self.client.post(reverse('update_projector', args=[self.projector.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_projectors'))
        self.projector.refresh_from_db()
        self.assertEqual(self.projector.name, 'Updated Projector')
        self.assertEqual(self.projector.description, 'Updated description')
        self.assertEqual(self.projector.quantity, 8)
