from django.shortcuts import render, redirect

def home(request):
    # if request.user.is_authenticated:
    #     if request.user.groups.filter(name='Vendedor').exists():
    #         return redirect('seller:dashboard')
    return render(request, 'index.html')