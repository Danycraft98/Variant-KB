from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^password_reset/$', auth_views.PasswordResetView, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_id>', views.user_profile, name='profile'),
]

