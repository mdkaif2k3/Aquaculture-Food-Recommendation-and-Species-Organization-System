import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from fish.models import FishSpecies


class Command(BaseCommand):
    help = "Update fish species descriptions from CSV"

    def handle(self, *args, **kwargs):
        csv_path = Path("fish/data/fish_species.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        updated = 0
        skipped = 0

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                common_name = row["common_name"].strip()
                description = row["description"].strip()

                try:
                    fish = FishSpecies.objects.get(common_name__iexact=common_name)
                except FishSpecies.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"Fish '{common_name}' not found. Skipping.")
                    )
                    skipped += 1
                    continue

                fish.description = description
                fish.save(update_fields=["description"])
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Descriptions updated: {updated}, skipped: {skipped}"
            )
        )