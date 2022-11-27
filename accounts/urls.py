from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:pk>/profile/', views.UserProfileView.as_view(), name="user_profile"),
    path('<int:pk>/update/', views.UpdateProfileView.as_view(), name="update_profile"),
    path('<int:pk>/delete/', views.DeleteProfileView.as_view(), name="delete_profile"),

]
