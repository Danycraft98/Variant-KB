from django.urls import include, path
from . import views

urlpatterns = [
	path('', include('django.contrib.auth.urls')),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('profile/<int:user_id>', views.user_profile, name='profile'),
]

