# Forms for user creation and user change in the accounts app.
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User

# Form for creating a new user.
class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

# Form for updating an existing user.
class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
