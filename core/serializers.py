from rest_framework import serializers
from .models import Issue, User, Review

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_active', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=True  # Default activation logic, or change as needed
        )
        return user

# Issue Serializer
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'address', 'photo', 'level', "category"]
class IssueDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'address', 'photo', 'level', 'status', 'reviews', "category"]

    def get_reviews(self, obj):
        # Get all reviews related to the issue
        reviews = Review.objects.filter(issue=obj)
        return ReviewSerializer(reviews, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", 'issue', 'text']