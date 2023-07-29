from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import RegCode, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User 

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('user-home')

    if request.method == 'POST':
        user = None
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        #print(f"EMAIL: {email}")
        try:
            user = User.objects.get(email=email)
            #print(f"EMAIL1: {user.email}")
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'User does not exist 1')
        #print(f"EMAIL2: {email}")
        

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url != None:                
                return redirect(next_url)
            return redirect('home')
            
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def user_home(request):
    context = {}
    return render(request, 'home.html', context)
def django_learning(request):
    context = {}
    return render(request, 'django_learning.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')

def home(request):
    context = {}
    return render(request, 'home.html', context)

def registerPage(request):
    if request.method == 'POST':
        
        form = UserRegisterForm(request.POST)
        reg_code = None
        # chk_reg_code = None
        if form.is_valid():
            new_user = form.save(commit=False)
            # check the registration code           
            reg_code = form.cleaned_data.get('RegistrationCode')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            # password1 = form.cleaned_data.get('password1')
            # password2 = form.cleaned_data.get('password2')
            
            if RegCode.objects.filter(reg_code=reg_code).exists():
                chk_reg_code = RegCode.objects.filter(reg_code=reg_code)
                 #print(f"USERNAME: {username} EMAIL: {email}")
                email = form.cleaned_data.get('email').lower()
                new_user.username = username
                form.save()
                messages.success(request, f"Your account {email} has been created! You may log in now.")
                return redirect('login')
            else:
                messages.error(request, f"Contact Administrator or utilize the correct Regn. Code/Information.")
                return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'login_register.html', {'form': form})


@login_required
def profile(request):
    
    # check if user has profile or create one
    user_profile = None 
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        print(f"UserProfile does not exists")
        user_profile = Profile(user=request.user, bio='Enter Bio')
        user_profile.save()
    

    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


