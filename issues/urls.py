
from django.urls import path
from . import views

urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('report/', views.report_issue, name='report_issue'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    # --- Naya URL ---
    path('register/', views.register, name='register'), # Registration page
  
    path('my_issues/', views.my_issues, name='my_issues'), # My Issues page

    path('profile/', views.profile_edit, name='profile_edit'),
    # --- End NEW URL ---
]