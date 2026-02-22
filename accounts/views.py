import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .form import UserRegisterForm, UserLoginForm, ProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Crear usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()

            # Crear el perfil asociado
            Profile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone'),
                address=form.cleaned_data.get('address')
            )

            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.save()

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente ✅")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def delete_profile_image(request):
   
    profile = request.user.profile

    
    image_path = profile.image.path


    if os.path.exists(image_path) and 'default.png' not in image_path:
        os.remove(image_path)

    
    profile.image = 'profile_pics/default.png'
    profile.save()

    messages.success(request, "Tu foto de perfil ha sido restablecida a la imagen por defecto ✅")
    return redirect('accounts:profile')


# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('products:product_list')
#     else:
#         form = UserLoginForm()
#     return render(request, 'accounts/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige según el grupo
                if user.groups.filter(name='Vendedor').exists():
                    return redirect('seller:dashboard')
                else:
                    return redirect('products:product_list')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente 👋")
    return redirect('accounts:login')