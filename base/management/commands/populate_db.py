import random
from datetime import datetime, timedelta
import pytz
from django.core.management.base import BaseCommand
from base.models import User, Project


class Command(BaseCommand):
    help = 'Populates the database with random generated data.'

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int,
                            help="The number of users that should be created.")
        parser.add_argument("--projects", type=int,
                            help="The number of clients that should be created.")

    def handle(self, *args, **options):

        # Users

        ROLES = [
            "PM", "DPM", "WD", "OM", "AM",
        ]
        FIRST_NAMES = ['Alice', 'Bob', 'Charlie', 'Dave',
                       'Eve', 'Frank', 'Grace', 'Heidi', 'Isaac', 'Judy']
        LAST_NAMES = ['Smith', 'Johnson', 'Brown', 'Lee', 'Garcia',
                      'Wilson', 'Davis', 'Perez', 'Taylor', 'Martinez']
        EMAIL_DOMAINS = ['example.com', 'test.com', 'dummy.com', 'sample.com']

        users = options['users'] if options['users'] else 0

        for i in range(0, users):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            user = User.objects.get_or_create(
                name=f'{first_name} {last_name}',
                email=f'{first_name}.{last_name}@{random.choice(EMAIL_DOMAINS)}',
                role=random.choice(ROLES)
            )

        # Projects

        PROJECT_NAMES = [
            "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"

        ]

        CLIENT_NAMES = [
            "Apex Innovations Inc.", "Brighter Horizons LLC", "Coastal Consulting Group", "Dream Builders Construction", "Elite Fitness Training", "Global Tech Solutions Corp.", "Hilltop Hospitality Group", "Innovative Marketing Strategies LLC", "Mountain View Properties", "Sapphire Financial Services Inc."
        ]

        projects = options['projects'] if options['projects'] else 0

        for i in range(0, projects):
            digital_project_managers = User.objects.filter(role="DPM")
            start = pytz.utc.localize(
                datetime.now() - timedelta(days=random.randint(0, 730)))

            project = Project.objects.create(
                name=F'Project {random.choice(PROJECT_NAMES)}-{random.randint(100, 999)}',
                client=random.choice(CLIENT_NAMES),
                project_manager=random.choice(digital_project_managers),
                description='Test Project',
            )
            project.started = start
            project.save()

        self.stdout.write(self.style.SUCCESS(
            "Successfully populated the database."))
