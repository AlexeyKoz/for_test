# Form for creating and validating vacations in the vacations app.
from django import forms
from django.utils import timezone
from .models import Vacation

# Form for the Vacation model.
class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ['country', 'description',
                  'start_date', 'end_date', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10000', 'step': '0.01'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    # Validate vacation form fields.
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        price = cleaned_data.get('price')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "End date must be after start date.")

            # Only validate start date for new vacations
            if not self.instance.pk and start_date < timezone.now().date():
                raise forms.ValidationError(
                    "Start date cannot be in the past.")

        if price is not None:
            if price < 0 or price > 10000:
                raise forms.ValidationError(
                    "Price must be between 0 and 10,000.")

        return cleaned_data
