# Tests for the core app.
from django.test import TestCase
from django.urls import reverse
from apps.vacations.models import Vacation
from apps.core.models import Country
from django.contrib.auth import get_user_model

User = get_user_model()


class HomePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com', password='testpass123')
        self.country = Country.objects.create(name='Testland')

    def test_home_page_with_vacations_positive(self):
        """Test that home page loads and displays vacations correctly."""
        # Create a test vacation
        vacation = Vacation.objects.create(
            country=self.country,
            description='Test vacation for home page',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        
        # Get the home page
        response = self.client.get(reverse('core:home'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test vacation for home page')
        self.assertContains(response, 'Testland')
        self.assertContains(response, '1000')

    def test_home_page_empty_vacations_negative(self):
        """Test that home page handles empty vacation list gracefully."""
        # Get the home page without any vacations
        response = self.client.get(reverse('core:home'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        # Should not contain any vacation data
        self.assertNotContains(response, 'Test vacation')
        # Should still load the page template
        self.assertTemplateUsed(response, 'core/home.html')
