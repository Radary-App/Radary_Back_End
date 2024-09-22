from django.urls import path
from .views import (
    SignUpView, LoginView,
    CreateProblemView, ProblemListView,
    CreateEmergencyView, EmergencyListView,
    CreateReviewView,
    Create911View,
    UpdateUserView, ProfileView, ProfilePersonalDataView,
    PaginatedProblemListView, PaginatedEmergencyListView,
    )

urlpatterns = [
    # login signup
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),

    # list views general 
    path('problem/<int:page_number>/', PaginatedProblemListView.as_view(), name='browse_problems'),
    path('emergency/<int:page_number>/', PaginatedEmergencyListView.as_view(), name='browse_emergencies'),
    path("problem/" , PaginatedProblemListView.as_view(), name="browse_problems"),
    path("emergency/" , PaginatedEmergencyListView.as_view(), name="browse_emergencies"),

    # list views per profile
    path('problem/all/', ProblemListView.as_view(), name='browse_problems'),
    path('emergency/all/', EmergencyListView.as_view(), name='browse_emergencies'),


    # create views
    path('problem/create/', CreateProblemView.as_view(), name='create_problem'),
    path('emergency/create/', CreateEmergencyView.as_view(), name='create_emergency'),

    
    # reviews
    path('problem/<int:problem_id>/review/', CreateReviewView.as_view(), name='problem_review'),


    # anonymous Emergency 
    path('911/', Create911View.as_view(), name='911_report'),
  
    # profile
    path("profile/update/", UpdateUserView.as_view(), name="profile"),
    path('profile/all/', ProfileView.as_view(), name='profile'),  
    path('profile/', ProfilePersonalDataView.as_view(), name='profilePersonal'),  
]
