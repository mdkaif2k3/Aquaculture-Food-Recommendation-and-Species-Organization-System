import csv
from django.core.management.base import BaseCommand
from fish.models import HabitatCondition
from pathlib import Path

class Command(BaseCommand):
    help = "Load habitat condition data from CSV into database"

    def handle(self, *args, **kwargs):
        csv_path = Path("fish/data/habitat_conditions.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                HabitatCondition.objects.create(
                    habitat_type=row["habitat_type"],
                    temp_min=row["temp_min"],
                    temp_max=row["temp_max"],
                    salinity=row["salinity"],
                    oxygen_level=row["oxygen_level"]
                )

        self.stdout.write(self.style.SUCCESS("Habitat Conditions data loaded successfully"))