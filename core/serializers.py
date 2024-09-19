from rest_framework import serializers
from .models import User, Problem, Emergency, Review, AI_Problem, AI_Emergency, Authority
import random, re
from Radary_AI import analyser
import base64
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'is_admin', 'date_of_birth', 'phone_number', 'governorate', 'markaz']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        phone_number_pattern = r'^01[0-2]\d{1,8}$'
        if not re.match(phone_number_pattern, data.get('phone_number', '')):
            raise serializers.ValidationError({"phone_number": "Phone number must be in the format '01X XXX XXXX'"})

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
    status = serializers.CharField(required=False, read_only=True)
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = Problem
        fields = ['coordinates', 'user_description', 'photo', 'status', 'id']

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
        print(problem.photo)
        image = get_img_data_(problem.photo)
        description, authority, priority = analyser.analyse_isuue(image)
        authority_name = 'City_council'
        subdivision = authority
        authority_object = Authority.objects.get(name=authority_name)
        ai_problem = AI_Problem.objects.create(
            report=problem,
            description=description,
            authority_name=authority_object,
            priority=priority,
            subdivision=subdivision if 'subdivision' in locals() else None,
        )
        return problem

def get_img_data_(IMG_PATH):
    uni_path = "media/" + str(IMG_PATH)
    with open(str(uni_path), "rb") as image_file:
        image_data = image_file.read()
    image_data_b64 = base64.b64encode(image_data).decode("utf-8")
    return image_data_b64

class EmergencySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = Emergency
        fields = ['coordinates', 'photo', 'id']

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

        print(emergency.photo)
        image = get_img_data_(emergency.photo)
        description, authority, level = analyser.analyse_accident(image)
        if authority not in ['Fire_station', 'Hospital']:
            authority = 'Police'
        authority_object = Authority.objects.get(name=authority)

        ai_emergency = AI_Emergency.objects.create(
            report=emergency,
            description=description,
            authority_name=authority_object,
            danger_level=level,
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
            is_solved=validated_data['is_solved'],
            difficulty=validated_data['difficulty'],
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
        user = User.objects.get(id=1)
        problem = Emergency.objects.create(
            user=user,
            coordinates=validated_data['coordinates'],
            photo=validated_data['photo'],
        )
        return problem
