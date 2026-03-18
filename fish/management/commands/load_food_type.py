import csv
from django.core.management.base import BaseCommand
from fish.models import FoodType
from pathlib import Path

class Command(BaseCommand):
    help = "Load food type data from CSV into database"

    def handle(self, *args, **kwargs):
        csv_path = Path("fish/data/food_types.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                FoodType.objects.create(
                    food_name=row["food_name"],
                    protein_percent=row["protein_percent"],
                    food_category=row["food_category"]
                )

        self.stdout.write(self.style.SUCCESS("Food type data loaded successfully"))