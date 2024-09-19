from django.urls import path
from .views import SignUpView, LoginView, CreateProblemView, ProblemListView, CreateEmergencyView, EmergencyListView, CreateReviewView, Create911View#, ProfileListView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),

    path('problem/create/', CreateProblemView.as_view(), name='create_problem'),
    path('problem/all/', ProblemListView.as_view(), name='browse_problems'),
    path('problem/<int:problem_id>/review/', CreateReviewView.as_view(), name='problem_review'),

    path('emergency/create/', CreateEmergencyView.as_view(), name='create_emergency'),
    path('emergency/all/', EmergencyListView.as_view(), name='browse_emergencies'),

    path('911/', Create911View.as_view(), name='911_report'),

    # path('profile/', ProfileListView.as_view(), name='profile_details'),
    # path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
    # path('profile/delete/', ProfileDeleteView.as_view(), name='delete_profile'),
]
