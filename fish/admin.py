from django.contrib import admin
from .models import UserLogin, FishSpecies, FoodType, Recommendation

# Register your models here.
admin.site.register(UserLogin)
admin.site.register(FishSpecies)
admin.site.register(FoodType)
admin.site.register(Recommendation)