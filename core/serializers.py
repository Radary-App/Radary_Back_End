from rest_framework import serializers
from .models import Report, User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'is_admin', 'date_of_birth', 'phone_number', 'governorate', 'markaz']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data['first_name'] + "@" + validated_data['last_name'] + '_' + str(range(0, 100))
        user = User.objects.create_user(
            username=username,
            firstname=validated_data['first_name'],
            lastname=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],


            is_admin=False,
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],

            governorate=validated_data['governorate'],
            markaz=validated_data['markaz'],
        )
        return user

# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['category', 'coordinates', 'user_description', 'photo']
