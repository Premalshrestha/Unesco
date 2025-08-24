from django.db import models
import datetime

# mother ko profile
class MotherProfile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_type = models.CharField(max_length=3)
    height = models.FloatField()
    weight = models.FloatField()
    medical_history = models.TextField()
    allergies = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    image = models.ImageField(upload_to='uploads/mother/')
    
    
    def __str__(self):
      return self.user.username








#pregnancy details
class PregnancyDetails(models.Model):
    pass



#health chekup details
class HealthCheckup(models.Model):
    pass


#nutrition tracking
class NutritionTracking(models.Model):
    pass


#mental health tracking
class MentalHealthTracking(models.Model):
    pass

#baby growth tracking
class BabyGrowthTracking(models.Model):
    pass


#baby health records
class BabyHealthRecords(models.Model):
    pass

#emergency services