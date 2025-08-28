# Management command to populate the database with users, countries, and vacations (with images).
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Country
from apps.vacations.models import Vacation
from django.utils import timezone
from datetime import timedelta
import random
import os
import shutil
from pathlib import Path
from django.conf import settings
from django.core.files import File

User = get_user_model()

# List of vacation data with country, description, and local image filename.
VACATION_DATA = [
    {
        'country': 'France',
        'description': 'Experience the magic of Paris with its iconic Eiffel Tower, world-class museums, and charming cafes. Enjoy the romantic atmosphere and rich cultural heritage.',
        'image_filename': 'france.jpg'
    },
    {
        'country': 'Italy',
        'description': 'Discover the eternal city of Rome with its ancient ruins, Vatican City, and delicious Italian cuisine. Immerse yourself in history and art.',
        'image_filename': 'italy.jpg'
    },
    {
        'country': 'Spain',
        'description': 'Enjoy the vibrant city of Barcelona with its unique architecture, beautiful beaches, and lively atmosphere. Perfect for art lovers and food enthusiasts.',
        'image_filename': 'spain.jpg'
    },
    {
        'country': 'Greece',
        'description': 'Visit the stunning Santorini with its white-washed buildings, blue domes, and breathtaking sunsets. A perfect romantic getaway.',
        'image_filename': 'greece.jpg'
    },
    {
        'country': 'Japan',
        'description': 'Explore Tokyo, a fascinating blend of traditional culture and cutting-edge technology. Experience unique cuisine and vibrant city life.',
        'image_filename': 'japan.jpg'
    },
    {
        'country': 'Thailand',
        'description': 'Relax in Phuket with its pristine beaches, crystal-clear waters, and luxurious resorts. Perfect for beach lovers and water sports enthusiasts.',
        'image_filename': 'thailand.jpg'
    },
    {
        'country': 'Australia',
        'description': 'Discover Sydney with its iconic Opera House, beautiful harbor, and stunning beaches. Experience the perfect blend of city and nature.',
        'image_filename': 'australia.jpg'
    },
    {
        'country': 'United States',
        'description': 'Visit New York City, the city that never sleeps. Experience world-famous landmarks, Broadway shows, and diverse cultural attractions.',
        'image_filename': 'united_states.jpg'
    },
    {
        'country': 'Canada',
        'description': 'Explore Vancouver with its stunning natural beauty, diverse culture, and outdoor activities. Perfect for nature lovers and adventure seekers.',
        'image_filename': 'canada.jpg'
    },
    {
        'country': 'Brazil',
        'description': 'Experience Rio de Janeiro with its famous beaches, vibrant culture, and iconic Christ the Redeemer statue. A perfect mix of nature and city life.',
        'image_filename': 'brazil.jpg'
    },
    {
        'country': 'South Africa',
        'description': 'Visit Cape Town with its stunning Table Mountain, beautiful beaches, and rich cultural heritage. Perfect for nature and adventure lovers.',
        'image_filename': 'south_africa.jpg'
    },
    {
        'country': 'Egypt',
        'description': 'Discover Cairo with its ancient pyramids, rich history, and vibrant culture. A perfect destination for history enthusiasts.',
        'image_filename': 'egypt.jpg'
    },
    {
        'country': 'India',
        'description': 'Experience the magic of Jaipur with its stunning palaces, rich culture, and vibrant markets. Perfect for cultural exploration.',
        'image_filename': 'india.jpg'
    },
    {
        'country': 'United Kingdom',
        'description': 'Visit London with its iconic landmarks, rich history, and diverse cultural attractions. Perfect for history and culture lovers.',
        'image_filename': 'united_kingdom.jpg'
    },
    {
        'country': 'Germany',
        'description': 'Explore Berlin with its rich history, vibrant art scene, and diverse cultural attractions. Perfect for history and culture enthusiasts.',
        'image_filename': 'germany.jpg'
    }
]

# Command to populate the database with initial data.


class Command(BaseCommand):
    help = 'Populates the database with initial data (countries, vacations)'

    # Main entry point for the management command.
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating vacations...')

        # Get the media root path
        media_root = Path(settings.MEDIA_ROOT)
        source_vacations_dir = media_root / 'vacations'

        # Ensure the vacations directory exists
        source_vacations_dir.mkdir(parents=True, exist_ok=True)

        # Clear existing vacations to avoid conflicts
        existing_vacations = Vacation.objects.all()
        if existing_vacations.exists():
            self.stdout.write('Clearing existing vacations...')
            existing_vacations.delete()
            self.stdout.write(self.style.SUCCESS('Existing vacations cleared'))

        start_date = timezone.now().date()

        # Create vacation objects and assign local images.
        for i, data in enumerate(VACATION_DATA):
            try:
                country, _ = Country.objects.get_or_create(
                    name=data['country'])
                vacation_start = start_date + timedelta(days=i*30)
                vacation_end = vacation_start + \
                    timedelta(days=random.randint(5, 14))
                price = random.randint(500, 9500)

                # Check if the image file exists
                source_image_path = source_vacations_dir / \
                    data['image_filename']
                if not source_image_path.exists():
                    self.stdout.write(self.style.WARNING(
                        f'Local image not found for {country.name}: {source_image_path}'))
                    continue

                vacation = Vacation.objects.create(
                    country=country,
                    description=data['description'],
                    start_date=vacation_start,
                    end_date=vacation_end,
                    price=price,
                    image=f'vacations/{data["image_filename"]}'
                )

                self.stdout.write(self.style.SUCCESS(
                    f'Successfully created vacation to {country.name} with local image'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error creating vacation for {data["country"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(
            'Database populated successfully'))
