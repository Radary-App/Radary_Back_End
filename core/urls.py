from django.urls import path
from .views import SignUpView, LoginView, IssueListView, CreateIssueView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('issues/', IssueListView.as_view(), name='browse_issues'),
    path('issue/create/', CreateIssueView.as_view(), name='create_issue'),

]
