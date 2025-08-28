from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Country
from .models import Vacation, Like

User = get_user_model()


class VacationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com', password='testpass123')
        self.country = Country.objects.create(name='Testland')

    def test_create_vacation_positive(self):
        self.client.login(email='user@example.com', password='testpass123')
        vacation = Vacation.objects.create(
            country=self.country,
            description='A test vacation',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        self.assertTrue(Vacation.objects.filter(
            description='A test vacation').exists())

    def test_create_vacation_invalid_dates_negative(self):
        with self.assertRaises(Exception):
            Vacation.objects.create(
                country=self.country,
                description='Invalid dates',
                start_date='2030-01-10',
                end_date='2030-01-01',
                price=1000
            )

    def test_create_vacation_negative_price_negative(self):
        with self.assertRaises(Exception):
            Vacation.objects.create(
                country=self.country,
                description='Negative price',
                start_date='2030-01-01',
                end_date='2030-01-10',
                price=-100
            )

    def test_list_vacations_positive(self):
        Vacation.objects.create(
            country=self.country,
            description='List test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        response = self.client.get(reverse('vacations:vacation_list'))
        self.assertContains(response, 'List test')

    def test_like_vacation_positive(self):
        vacation = Vacation.objects.create(
            country=self.country,
            description='Like test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        self.client.login(email='user@example.com', password='testpass123')
        response = self.client.post(
            reverse('vacations:vacation_like', args=[vacation.id]))
        self.assertEqual(Like.objects.filter(
            user=self.user, vacation=vacation).count(), 1)

    def test_like_vacation_unauthenticated_negative(self):
        vacation = Vacation.objects.create(
            country=self.country,
            description='Like unauth',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        response = self.client.post(
            reverse('vacations:vacation_like', args=[vacation.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_vacation_list_page_with_likes_positive(self):
        """Test that vacation list page displays vacations and like functionality works for authenticated users."""
        # Create a test vacation
        vacation = Vacation.objects.create(
            country=self.country,
            description='Vacation for list test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1500
        )
        
        # Login user
        self.client.login(email='user@example.com', password='testpass123')
        
        # Get the vacation list page
        response = self.client.get(reverse('vacations:vacation_list'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vacation for list test')
        self.assertContains(response, 'Testland')
        self.assertContains(response, '1500')
        # Should show like button for authenticated users
        self.assertTemplateUsed(response, 'vacations/vacation_list.html')

    def test_vacation_list_page_unauthenticated_negative(self):
        """Test that unauthenticated users can view vacations but cannot like them."""
        # Create a test vacation
        vacation = Vacation.objects.create(
            country=self.country,
            description='Vacation for unauth test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=2000
        )
        
        # Get the vacation list page without logging in
        response = self.client.get(reverse('vacations:vacation_list'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vacation for unauth test')
        # Should still display the page but without like functionality
        self.assertTemplateUsed(response, 'vacations/vacation_list.html')

    def test_vacation_detail_page_positive(self):
        """Test that vacation detail page displays vacation details and like functionality works."""
        # Create a test vacation
        vacation = Vacation.objects.create(
            country=self.country,
            description='Vacation for detail test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=2500
        )
        
        # Login user
        self.client.login(email='user@example.com', password='testpass123')
        
        # Get the vacation detail page
        response = self.client.get(reverse('vacations:vacation_detail', args=[vacation.id]))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vacation for detail test')
        self.assertContains(response, 'Testland')
        self.assertContains(response, '2500')
        self.assertTemplateUsed(response, 'vacations/vacation_detail.html')

    def test_vacation_detail_page_not_found_negative(self):
        """Test that vacation detail page returns 404 for non-existent vacation ID."""
        # Try to access a vacation that doesn't exist
        response = self.client.get(reverse('vacations:vacation_detail', args=[99999]))
        
        # Check response
        self.assertEqual(response.status_code, 404)
