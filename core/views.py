from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from .models import Token, User, Problem, Emergency, AI_Emergency, AI_Problem, Review, Authority, Authority_Locations
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from .serializers import UserSerializer, ProblemSerializer, EmergencySerializer, ReviewSerializer, NOOSerializer
from django.utils.crypto import get_random_string
from .authentication import TokenAuthentication

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if phone_number is None or password is None:
            raise Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            # Generate a new token
            token = get_random_string(255)
            Token.objects.update_or_create(user=user, defaults={'token': token})
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateProblemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request):
        print("Creating report")
        user = request.user
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProblemListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_problems = Problem.objects.all().filter(user=request.user)
        serializer = ProblemSerializer(all_problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CreateEmergencyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Creating Emergency")
        user = request.user
        serializer = EmergencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, report=request.data.get('report'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmergencyListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_emergencies = Emergency.objects.all().filter(user=request.user)
        serializer = ProblemSerializer(all_emergencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CreateReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, problem_id):
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)


        serializer = ReviewSerializer(data=request.data, context={
            'related_user': request.user,
            'related_report': problem
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class Create911View(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Creating 911")
        serializer = NOOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(report=request.data.get('report'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class ProfileListView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         return Response(UserSerializer(user).data)
    
# class ProfileUpdateView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         user = request.user
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ProfileDeleteView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def delete(self, request):
#         user = request.user
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

