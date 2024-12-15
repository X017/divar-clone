from rest_framework import serializers
from listing.models import Listing, City, Place , Category
from accounts.models import CustomUser

class ListingSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    city  = serializers.SlugRelatedField(slug_field='city',queryset=City.objects.all())
    place = serializers.SlugRelatedField(slug_field='section',queryset=Place.objects.all())
    category = serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())
    class Meta:
        model = Listing
        fields = ['author', 'title', 'category', 'city', 'place', 'price', 'description']

    def get_author(self, obj):
        return obj.author.username

    def get_contact(self, obj):
        return obj.contact.phone_number  # Assuming contact is a user and you want to get the phone number
    def validate(self,data):
        if data['place'].city != data['city']:
            raise serializers.ValidationError("The place does not belong to the selected city.")
        return data

class SignInSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # password = serializers.CharField()
    # phone_number = serializers.CharField()
# 
    class Meta:
        model = CustomUser
        fields = ('username','password','phone_number')
        # extra_kwargs = {'password':{'write_only':True}}


        def save(self, validated_data):
            password = validated_data['password']
            print(f"**{password}**")
            user = CustomUser.objects.create(
                username = validated_data['username'],
                phone_number = validated_data['phone_number'],

            )
            user.set_password(password=validated_data['password'])
            user.save()
            return user 
         # Hash the raw password user.save() return 