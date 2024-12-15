from django.contrib import admin
from .models import City, Place,Category,Listing

admin.site.register(Place)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Listing)


