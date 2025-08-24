from django.contrib import admin
from .models import MotherProfile, PregnancyDetails, HealthCheckup, NutritionTracking, MentalHealthTracking, BabyGrowthTracking, BabyHealthRecords

# Register your models here.
admin.site.register(MotherProfile)
admin.site.register(PregnancyDetails)
admin.site.register(HealthCheckup)
admin.site.register(NutritionTracking)
admin.site.register(MentalHealthTracking)
admin.site.register(BabyGrowthTracking)
admin.site.register(BabyHealthRecords)