from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    


class City(models.Model):
    city = models.CharField(max_length=110)

    def __str__(self):
        return f"{self.city}"


class Place(models.Model):
    section = models.CharField(max_length=110)
    city = models.ForeignKey(City,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.city}"

class Listing(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    place = models.ForeignKey(Place,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    description = models.TextField(default='')
    contact = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.title} - {self.category}"
    


