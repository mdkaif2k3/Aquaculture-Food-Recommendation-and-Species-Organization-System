import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from fish.models import TrainingSample, FishSpecies, FoodType


class Command(BaseCommand):
    help = "Load training samples from CSV"

    def handle(self, *args, **kwargs):
        csv_path = Path("fish/data/training_data.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                fish = FishSpecies.objects.get(id=row["fish_id"])
                food = FoodType.objects.get(id=row["food_id"])

                TrainingSample.objects.create(
                    fish=fish,
                    water_type=row["water_type"],
                    farm_type=row["farm_type"],
                    farm_size=float(row["farm_size"]),
                    water_temperature=float(row["water_temperature"]),
                    food=food
                )

        self.stdout.write(self.style.SUCCESS("Training samples loaded successfully"))