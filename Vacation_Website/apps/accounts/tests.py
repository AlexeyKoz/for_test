# Tests for the accounts app.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Test cases for the custom user model and authentication.
class UserTests(TestCase):
    # Test creating a user successfully.
    def test_create_user_positive(self):
        user = User.objects.create_user(
            email='test@example.com', password='testpass123')
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertTrue(user.check_password('testpass123'))

    # Test creating a user with duplicate email (should fail).
    def test_create_user_duplicate_email_negative(self):
        User.objects.create_user(
            email='test@example.com', password='testpass123')
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com', password='testpass456')



    # Test updating user profile successfully.
    def test_profile_update_positive(self):
        user = User.objects.create_user(
            email='test@example.com', password='testpass123', first_name='Old')
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(reverse('accounts:profile'), {
                                    'first_name': 'New', 'last_name': 'User', 'email': 'test@example.com'})
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New')

    # Test updating profile while unauthenticated (should fail).
    def test_profile_update_unauthenticated_negative(self):
        response = self.client.post(
            reverse('accounts:profile'), {'first_name': 'New'})
        self.assertNotEqual(response.status_code, 200)

    def test_login_page_positive(self):
        """Test that login page works with correct credentials."""
        # Create a user
        User.objects.create_user(
            email='login@example.com', password='testpass123')
        
        # Get the login page
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # Submit login form with correct credentials
        response = self.client.post(reverse('accounts:login'), {
            'username': 'login@example.com',  # Django uses username field for email
            'password': 'testpass123'
        })
        
        # Should redirect to home page after successful login
        self.assertRedirects(response, reverse('core:home'))

    def test_login_page_wrong_credentials_negative(self):
        """Test that login page fails with incorrect credentials."""
        # Create a user
        User.objects.create_user(
            email='login@example.com', password='testpass123')
        
        # Submit login form with wrong password
        response = self.client.post(reverse('accounts:login'), {
            'username': 'login@example.com',
            'password': 'wrongpassword'
        })
        
        # Should stay on login page with error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        # Check for error message
        self.assertContains(response, 'One of the parameters is not correct')

    def test_signup_page_positive(self):
        """Test that signup page works with valid data."""
        # Get the signup page
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        
        # Submit signup form with valid data
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        # Should redirect to login page after successful signup
        self.assertRedirects(response, reverse('accounts:login'))
        
        # Check that user was created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_signup_page_duplicate_email_negative(self):
        """Test that signup page fails with duplicate email."""
        # Create a user first
        User.objects.create_user(
            email='existing@example.com', password='testpass123')
        
        # Try to signup with same email
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'existing@example.com',
            'password1': 'testpass456',
            'password2': 'testpass456',
            'first_name': 'Another',
            'last_name': 'User'
        })
        
        # Should stay on signup page with error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        # Check for form errors
        self.assertContains(response, 'User with this Email already exists')
