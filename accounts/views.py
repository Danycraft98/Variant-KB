from django.contrib.auth.decorators import login_required
from .models import User
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        User.objects.create_user(request.POST.get('username', ''),
                                 password=request.POST.get('password1', ''),
                                 email=request.POST.get('email', ''))
        return redirect('/accounts/login')
    return render(request,'registration/signup.html')


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'registration/profile.html', {"user": user})
