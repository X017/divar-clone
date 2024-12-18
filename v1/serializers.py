from rest_framework import serializers
from listing.models import Listing, City, Place , Category
from accounts.models import CustomUser


class ListingSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='city', queryset=City.objects.all())
    place = serializers.SlugRelatedField(slug_field='section', queryset=Place.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    description = serializers.CharField(required=True)
    class Meta:
        model = Listing
        fields = ['title', 'category', 'city', 'place', 'price', 'description', 'phone_number', 'author','uid']
        read_only_fields = ['author', 'phone_number', 'uid','is_deleted']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        validated_data['phone_number'] = request.user.phone_number
        return super().create(validated_data)

    def validate(self, data):
        if data['place'].city != data['city']:
            raise serializers.ValidationError("The place does not belong to the selected city.")
        return data

    

class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username','password','phone_number')
        extra_kwargs = {'password':{'write_only':True}}


    def create(self, validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'],
            phone_number = validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user 
     # Hash the raw password user.save() return 
