from django.db import models
from django.conf import settings
from django.utils import timezone

class UserLogin(models.Model):
    username = models.CharField(max_length = 50, unique = True, default = '')
    email = models.CharField(max_length = 50, unique = True, default = '')
    password = models.CharField(max_length = 255, default = '')
    image = models.ImageField(upload_to="user_images/", null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(default = timezone.now)

class FishSpecies(models.Model):
    common_name = models.CharField(max_length = 100, default = '')
    scientific_name = models.CharField(max_length = 150, default = '')
    taxonomy_family = models.CharField(max_length = 100, default = '')
    habitat = models.CharField(max_length = 100, default = '')
    water_type = models.CharField(max_length = 50, default = '')
    threatened_status = models.CharField(max_length = 50, default = '')
    fish_img = models.ImageField(upload_to="fish_images/", null=True, blank=True)
    description = models.TextField(blank = True)

class FishAlias(models.Model):
    fish = models.ForeignKey(FishSpecies, on_delete=models.CASCADE, related_name='aliases')
    alias_name = models.CharField(max_length = 100, default = '')

class HabitatCondition(models.Model):
    habitat_type = models.CharField(max_length = 100, default = '')
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    salinity = models.CharField(max_length = 50, default = '')
    oxygen_level = models.CharField(max_length = 50, default = '')

class FoodType(models.Model):
    food_name = models.CharField(max_length = 100, default = '')
    protein_percent = models.IntegerField()
    food_category = models.CharField(max_length = 100, default = '')
    food_img = models.ImageField(upload_to="food_images/", null=True, blank=True)

class FishFoodMapping(models.Model):
    fish = models.ForeignKey(FishSpecies, on_delete = models.CASCADE)
    food = models.ForeignKey(FoodType, on_delete = models.CASCADE)
    suitability_score = models.IntegerField(default = 0)

class Recommendation(models.Model):
    user = models.ForeignKey("UserLogin", on_delete = models.CASCADE, related_name = "recommendations")
    fish = models.ForeignKey("FishSpecies", on_delete = models.CASCADE, related_name = "recommendations")
    food = models.ForeignKey("FoodType", on_delete = models.CASCADE, related_name = "recommendations", null=True)

    # Input
    farm_type = models.CharField(max_length = 50, default = '')
    farm_size = models.FloatField(help_text="Farm size in acres or sq.m")
    water_temperature = models.FloatField(null = True, blank = True, help_text = "Water temperature in Celsius")

    # Output
    recommended_food_name = models.CharField(max_length = 100, null = True, blank = True)
    confidence = models.FloatField(null = True, blank = True)
    status = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)

class TrainingSample(models.Model):
    fish = models.ForeignKey("FishSpecies", on_delete = models.CASCADE)
    water_type = models.CharField(max_length = 25, default = '')
    farm_type = models.CharField(max_length = 50, default = '')
    farm_size = models.FloatField()
    water_temperature = models.FloatField()
    food = models.ForeignKey("FoodType", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class RecentHistory(models.Model):
    user = models.ForeignKey("UserLogin", on_delete = models.CASCADE)
    fish = models.ForeignKey("FishSpecies", on_delete = models.CASCADE)
    action = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)