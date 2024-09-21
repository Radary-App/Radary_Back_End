from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        print(serializer.errors)
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
        
        serializer = NOOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(report=request.data.get('report'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class PaginatedProblemListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, page_number=1):
        """Get paginated list of problems"""
        problems = Problem.objects.all().order_by('-created_at')
        paginator = Paginator(problems, 20)  # 20 problems per page

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            return Response({"error": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)
        except EmptyPage:
            return Response({"error": "No more problems"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProblemSerializer(page.object_list, many=True)
        return Response({
            "page_number": page_number,
            "total_pages": paginator.num_pages,
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class PaginatedEmergencyListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, page_number=1):
        """Get paginated list of emergencies"""
        emergencies = Emergency.objects.all().order_by('-created_at')
        paginator = Paginator(emergencies, 20)  # 20 emergencies per page

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            return Response({"error": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)
        except EmptyPage:
            return Response({"error": "No more emergencies"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmergencySerializer(page.object_list, many=True)
        return Response({
            "page_number": page_number,
            "total_pages": paginator.num_pages,
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
       
        serializer = UserSerializer(user, data=request.data, partial=True)  # `partial=True` allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,req):

        user = req.user

 
        serializerEmergency = EmergencySerializer(user.emergency_set.all(), many=True)  
        serializerProblem = ProblemSerializer(user.problem_set.all(), many=True)


        return Response({"emergency": serializerEmergency.data, "problem": serializerProblem.data}, status=status.HTTP_200_OK)
    



class ProfilePersonalDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,req):
        user = req.user 
        serializerUser = UserSerializer(user)   
        return Response({"user": serializerUser.data}, status=status.HTTP_200_OK)