import csv
from django.core.management.base import BaseCommand
from fish.models import FishAlias, FishSpecies
from pathlib import Path

class Command(BaseCommand):
    help = "Load fish alias data from CSV into database"

    def handle(self, *args, **kwargs):
        csv_path = Path("fish/data/fish_aliases.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                fish_id = row["fish_id"].strip()
                alias = row["alternate_name"].strip()

                try:
                    fish = FishSpecies.objects.get(id=fish_id)
                except FishSpecies.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fish with id {fish_id} not found. Skipping alias '{alias}'."
                        )
                    )
                    continue

                FishAlias.objects.create(
                    fish=fish,            
                    alias_name=alias      
                )

        self.stdout.write(self.style.SUCCESS("Fish Alias data loaded successfully"))