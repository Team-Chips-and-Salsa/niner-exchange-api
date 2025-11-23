from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models.user import CustomUser
from core.models.meetup_location import MeetupLocation

class ExchangeZoneTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='password123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        # Create regular user
        self.regular_user = CustomUser.objects.create_user(
            email='user@example.com',
            password='password123',
            first_name='Regular',
            last_name='User'
        )
        
        # Create exchange zone
        self.exchange_zone = MeetupLocation.objects.create(
            name='Test Zone',
            description='Test Description',
            latitude=35.3075,
            longitude=-80.7337,
            is_active=True
        )
        
        self.detail_url = reverse('admin-exchange-zone-detail-view', kwargs={'pk': self.exchange_zone.pk})

    def test_update_exchange_zone_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Updated Zone',
            'description': 'Updated Description',
            'latitude': 35.0000,
            'longitude': -80.0000,
            'is_active': True
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exchange_zone.refresh_from_db()
        self.assertEqual(self.exchange_zone.name, 'Updated Zone')

    def test_delete_exchange_zone_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.exchange_zone.refresh_from_db()
        self.assertFalse(self.exchange_zone.is_active)

    def test_update_exchange_zone_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Updated Zone'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_exchange_zone_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
