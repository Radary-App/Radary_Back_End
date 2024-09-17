from django.urls import path
from .views import SignUpView, LoginView, IssueListView, CreateIssueView, IssueDetailView, CreateReviewView, UserIssueListView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('issues/', IssueListView.as_view(), name='browse_issues'),
    path('issue/create/', CreateIssueView.as_view(), name='create_issue'),
    path('issue/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('issue/<int:pk>/add/review/', CreateReviewView.as_view(), name='issue_review'),
    path("issue/profile/" , UserIssueListView.as_view(), name="user_issues"),
]
