import csv
from django.core.management.base import BaseCommand
from fish.models import FishSpecies
from pathlib import Path


class Command(BaseCommand):
    help = "Load fish species data from CSV into database"

    def handle(self, *args, **kwargs):
        csv_path = Path("fish/data/fish_species.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                FishSpecies.objects.create(
                    common_name=row["common_name"],
                    scientific_name=row["scientific_name"],
                    taxonomy_family=row["taxonomy"],
                    habitat=row["habitat"],
                    water_type=row["water_type"],
                    threatened_status=row["threatened_status"]
                )

        self.stdout.write(self.style.SUCCESS("Fish species data loaded successfully"))