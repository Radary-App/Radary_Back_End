from rest_framework import serializers
from .models import User, Problem, Emergency, Review, AI_Problem, AI_Emergency
import random, re, logging
from Radary_AI import main as AI_Engine
from datetime import datetime
logger = logging.getLogger('core')



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', "image", 'email',  'date_of_birth', 'phone_number', 'governorate', 'markaz']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        phone_number = data.get('phone_number', None)
        if phone_number is not None:
            cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))
            if len(cleaned_phone_number) < 10 or len(cleaned_phone_number) > 14:
                raise serializers.ValidationError({
                    'phone_number': "Phone number must be between 11 and 14 digits."
                })

        return data
    def create(self, validated_data):
        random_number = random.randint(1, 100000)
        username = validated_data['first_name'] + "@" + validated_data['last_name'] + '_' + str(random_number)
        
        user = User.objects.create_user(
            username=username,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],

            is_admin=False,
            image = validated_data['image'] if 'image' in validated_data else None,
            date_of_birth=validated_data['date_of_birth'] if 'date_of_birth' in validated_data else None,
            email=validated_data['email'] if 'email' in validated_data else None,
            governorate=validated_data['governorate'] if 'governorate' in validated_data else None,
            markaz=validated_data['markaz'] if 'markaz' in validated_data else None,
        )
        return user



# Problem Serializer
class ProblemSerializer(serializers.ModelSerializer):
    ai_description_english = serializers.SerializerMethodField()
    ai_description_arabic = serializers.SerializerMethodField()
    class Meta:
        model = Problem
        fields = [
            'coordinates',
            'status',
            'user_description',
            'photo', 
            'created_at',
            'status',
            'id',
            'ai_description_english',
            'ai_description_arabic',
        ]

    def get_ai_description_english(self, obj):
        try:
            ai_problem = AI_Problem.objects.get(report=obj)
            return ai_problem.description 
        except AI_Problem.DoesNotExist:
            return None
        
    def get_ai_description_arabic(self, obj):
        try:
            ai_problem = AI_Problem.objects.get(report=obj)
            arabic_description = AI_Engine.translate(ai_problem.description)
            return arabic_description
        except AI_Problem.DoesNotExist:
            return None

    def validate(self, data):
        coordinates_pattern = r'^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$'
        if not re.match(coordinates_pattern, data.get('coordinates', '')):
            raise serializers.ValidationError({"coordinates": "Coordinates must be in the format 'lat, long'"})
        if 'photo' not in data:
            raise serializers.ValidationError({"photo": "Photo is required"})
        return data

    def create(self, validated_data):
        problem = Problem.objects.create(
            user=validated_data['user'],
            coordinates=validated_data['coordinates'],
            photo=validated_data['photo'],
            user_description=validated_data['user_description'] if 'user_description' in validated_data else None
        )
        return problem

class EmergencySerializer(serializers.ModelSerializer):
    ai_description_english = serializers.SerializerMethodField()
    ai_description_arabic = serializers.SerializerMethodField()
    class Meta:
        model = Emergency
        fields = ['coordinates', 'photo', 'id', 'ai_description_english', 'ai_description_arabic']

    def get_ai_description_arabic(self, obj):
        try:
            ai_emergency = AI_Emergency.objects.get(report=obj)
            return ai_emergency.description
        except AI_Emergency.DoesNotExist:
            return None

    def get_ai_description_english(self, obj):
        try:
            ai_emergency = AI_Emergency.objects.get(report=obj)
            arabic_description = AI_Engine.translate(ai_emergency.description)
            return arabic_description
        except AI_Emergency.DoesNotExist:
            return None

    def validate(self, data):
        coordinates_pattern = r'^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$'
        if not re.match(coordinates_pattern, data.get('coordinates', '')):
            raise serializers.ValidationError({"coordinates": "Coordinates must be in the format 'lat, long'"})
        if 'photo' not in data:
            raise serializers.ValidationError({"photo": "Photo is required"})
        return data

    def create(self, validated_data):
        emergency = Emergency.objects.create(
            user=validated_data['user'],
            coordinates=validated_data['coordinates'],
            photo=validated_data['photo'],
        )
        return emergency


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['is_solved', 'difficulty', 'comment']

    def create(self, validated_data):
        related_user = self.context['related_user']
        related_report = self.context['related_report']

        review = Review.objects.create(
            related_user=related_user,
            related_report=related_report,
            is_solved=validated_data.get("is_solved", False),
            difficulty=validated_data.get("difficulty", None),
            comment=validated_data['comment'] if 'comment' in validated_data else None
        )
        return review
    

class NOOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = ['coordinates', 'photo']

    def validate(self, data):
        coordinates_pattern = r'^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$'
        if not re.match(coordinates_pattern, data.get('coordinates', '')):
            raise serializers.ValidationError({"coordinates": "Coordinates must be in the format 'lat, long'"})
        if 'photo' not in data:
            raise serializers.ValidationError({"photo": "Photo is required"})
        return data

    def create(self, validated_data):
        try:
            user = User.objects.get(id=1)
        except:
            user = User.objects.create_user(
                    username='emergency_user',
                    email='emergency_user@example.com',
                    password='12345678',
                    first_name = 'Emergency',
                    last_name = 'User',
                    phone_number = '111111111111',
                    date_of_birth = datetime.date(year=2000, month=1, day=1)
                )
            user.save()


        problem = Emergency.objects.create(
            user=user,
            coordinates=validated_data['coordinates'],
            photo=validated_data['photo'],
        )
        return problem
