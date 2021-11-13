from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.views.generic.detail import DetailView
from django.views import View
from .forms import UserForm, ProfileForm


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            auth.login(request, user)
            return redirect('/')
        return render(request, 'user/signup.html')
    return render(request, 'user/signup.html')

# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'user/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'user/login.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('/')

# home
def home(request):
    return render(request, '/')

class ProfileView(DetailView):
    context_object_name = 'profile_user'
    model = User
    template_name = 'user/profile.html'

class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

        if hasattr(user, 'profile'):
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname': profile.nickname,
                'image': profile.image,
                'bio': profile.bio,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'user/profile_update.html', {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        u = User.objects.get(id=request.user.pk)
        user_form = UserForm(request.POST, instance=u)

        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = u
            profile.save()

        return redirect('user:profile', pk=request.user.pk)
