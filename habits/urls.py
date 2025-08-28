from habits.apps import HabitsConfig
from habits.views import (ListPrivateAPIViewPermissions, ListPublicAPIViewPermissions, CreateAPIViewPermissions,
                          RetrieveAPIViewPermissions, UpdateAPIViewPermissions, DestroyAPIViewPermissions,
                          )
from django.urls import path

app_name = HabitsConfig.name


urlpatterns = [
path('private_habits/', ListPrivateAPIViewPermissions.as_view(), name='private-habits'),
path('public_habits/', ListPublicAPIViewPermissions.as_view(), name='public-habits'),
path('create/', CreateAPIViewPermissions.as_view(), name='create-habit'),
path('retrieve/<int:pk>/', RetrieveAPIViewPermissions.as_view(), name='retrieve-habit'),
path('update/<int:pk>/', UpdateAPIViewPermissions.as_view(), name='update-habit'),
path('destroy/<int:pk>/', DestroyAPIViewPermissions.as_view(), name='destroy-habit'),
]


