from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Country
from apps.vacations.models import Vacation, Like
import psycopg2

User = get_user_model()


class Command(BaseCommand):
    help = 'Migrate data from old database structure'

    def handle(self, *args, **options):
        # Connect to old database
        conn = psycopg2.connect(
            dbname="project_db",
            user="postgres",
            password="1234",
            host="localhost"
        )
        cursor = conn.cursor()

        # Migrate countries
        self.stdout.write('Migrating countries...')
        cursor.execute("SELECT id, name FROM countries")
        for row in cursor.fetchall():
            Country.objects.get_or_create(
                id=row[0],
                defaults={'name': row[1]}
            )

        # Migrate users
        self.stdout.write('Migrating users...')
        cursor.execute("""
            SELECT id, first_name, last_name, email, password, role_id 
            FROM users
        """)
        for row in cursor.fetchall():
            user, created = User.objects.get_or_create(
                email=row[3],
                defaults={
                    'first_name': row[1] or '',
                    'last_name': row[2] or '',
                    'is_staff': row[5] == 1,  # Admin role
                    'is_superuser': row[5] == 1,
                }
            )
            if created:
                # Set password (you'll need to reset these)
                user.set_password('temporary123')
                user.save()

        # Migrate vacations
        self.stdout.write('Migrating vacations...')
        cursor.execute("""
            SELECT id, country_id, description, start_date, end_date, price, image_url
            FROM vacations
        """)
        for row in cursor.fetchall():
            try:
                country = Country.objects.get(id=row[1])
                Vacation.objects.get_or_create(
                    id=row[0],
                    defaults={
                        'country': country,
                        'description': row[2],
                        'start_date': row[3],
                        'end_date': row[4],
                        'price': row[5],
                        # Note: image_url will need to be handled separately
                    }
                )
            except Country.DoesNotExist:
                self.stdout.write(f'Country {row[1]} not found for vacation {row[0]}')

        # Migrate likes
        self.stdout.write('Migrating likes...')
        cursor.execute("SELECT user_id, vacation_id FROM likes")
        for row in cursor.fetchall():
            try:
                user = User.objects.get(id=row[0])
                vacation = Vacation.objects.get(id=row[1])
                Like.objects.get_or_create(
                    user=user,
                    vacation=vacation
                )
            except (User.DoesNotExist, Vacation.DoesNotExist) as e:
                self.stdout.write(f'Error migrating like: {e}')

        cursor.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Data migration completed!'))