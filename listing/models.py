from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    city = models.CharField(max_length=110)

    def __str__(self):
        return self.city

class Place(models.Model):
    section = models.CharField(max_length=110)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city} - {self.section}"

class Listing(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_listings')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    description = models.TextField(default='')
    phone_number = models.CharField(max_length=15, blank=True, null=True) # Use CharField
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.category.name} - {self.phone_number} created at {self.created_at}"
    
    def save(self,*args, **kwargs):
        if self.place.city != self.city:
            raise ValidationError("The place does not belong to the selected city.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
