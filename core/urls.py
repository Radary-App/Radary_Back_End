from django.urls import path
from .views import SignUpView, LoginView, ReportListView, CreateReportView, ProfileListView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('reports/', ReportListView.as_view(), name='browse_reports'),
    path('reports/create/', CreateReportView.as_view(), name='create_report'),
    
    path('profile/', ProfileListView.as_view(), name='profile_details'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='delete_profile'),

]
