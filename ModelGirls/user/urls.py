from django.urls import path
from django.views.generic.detail import DetailView

from .views import *
from .models import Profile

app_name = 'user'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/<int:pk>', ProfileView.as_view(), name="profile"),
    path('profile/update', ProfileUpdateView.as_view(), name="profile_update")
]
