from django.urls import path

from users.views import CreateUser, MyTokenObtainPairView, RetrieveUserAPIView, UsersListAPIView

urlpatterns = [
    path('users/', UsersListAPIView.as_view(), name='list-users'),
    path('users/<int:pk>/', RetrieveUserAPIView.as_view(), name='retrieve-user'),
    path('register/', CreateUser.as_view(), name='register-user'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]