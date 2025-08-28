from django.db import models


# Model representing a country.
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    # Return the string representation of the country.
    def __str__(self):
        return self.name