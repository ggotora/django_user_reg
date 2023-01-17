from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "users/home.html")

@login_required(login_url='login')
def profile(request):
    print(request.path_info)
    return render(request, 'users/profile.html')

def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your Account was updated")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        profile_path = request.path_info
        
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile_path": profile_path 
    }
    return render(request, 'users/profile.html', context)



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}, login")
            return redirect('login')
            

    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {'form': form })
    
