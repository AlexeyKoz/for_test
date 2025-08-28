# Models for vacations and likes in the vacations app.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.models import Country

User = get_user_model()

# Model representing a vacation.
class Vacation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='vacations')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vacations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Vacation'
        verbose_name_plural = 'Vacations'

    # Validate vacation fields.
    def clean(self):
        # Price validation
        if self.price < 0 or self.price > 10000:
            raise ValidationError("Price must be between 0 and 10,000.")
        # Date validation
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date.")
        # Past date validation
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")

    # Save the vacation after validation.
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # String representation of the vacation.
    def __str__(self):
        return f"{self.country.name} - {self.start_date} to {self.end_date}"

    # Return the number of likes for the vacation.
    @property
    def likes_count(self):
        return self.likes.count()

    # Check if the vacation is liked by a user.
    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

# Model representing a like on a vacation.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vacation')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    # String representation of the like.
    def __str__(self):
        return f"{self.user.email} likes {self.vacation}"