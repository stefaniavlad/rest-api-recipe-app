"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        attempts = 0
        max_attempts = 30

        while not db_up and attempts < max_attempts:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                attempts += 1
                self.stdout.write(f'Database unavailable, waiting 1 second... (Attempt {attempts})')
                time.sleep(1)

        if db_up:
            self.stdout.write(self.style.SUCCESS('Database available'))
        else:
            self.stderr.write(self.style.ERROR('Database not available after 30 attempts. Exiting.'))
            exit(1)
