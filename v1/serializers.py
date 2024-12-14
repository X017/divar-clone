from rest_framework import serializers
from listing.models import Listing, City, Place , Category

class ListingSerializer(serializers.ModelSerializer):
    #author = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    city  = serializers.SlugRelatedField(slug_field='city',queryset=City.objects.all())
    place = serializers.SlugRelatedField(slug_field='section',queryset=Place.objects.all())
    category = serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())
    class Meta:
        model = Listing
        fields = ['title', 'category', 'city', 'place', 'price', 'description', 'contact']

    def get_author(self, obj):
        return obj.author.username

    def get_contact(self, obj):
        return obj.contact.phone_number  # Assuming contact is a user and you want to get the phone number
    def validate(self,data):
        if data['place'].city != data['city']:
            raise serializers.ValidationError("The place does not belong to the selected city.")
        return data