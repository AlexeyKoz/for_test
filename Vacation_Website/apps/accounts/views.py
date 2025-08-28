from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import LoginView

# Views for user registration, login, and profile management.

# View for user signup.
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    # Handle valid signup form submission.
    def form_valid(self, form):
        messages.success(
            self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)

# View for user profile update.
class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    # Get the current user object.
    def get_object(self):
        return self.request.user

    # Handle valid profile update form submission.
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

# View for custom user login.
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    # Handle invalid login form submission.
    def form_invalid(self, form):
        messages.error(
            self.request, 'One of the parameters is not correct, please try again.')
        return super().form_invalid(form)
