from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import Task

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == "POST":
        # Obtener datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if not all([username, email, password1, password2]):
            messages.error(request, "Todos los campos son obligatorios")
            return render(request, "signup.html")
        
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, "signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado")
            return render(request, "signup.html")
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password1
            )
            login(request, user)
            messages.success(request, "Cuenta creada. ¡Bienvenido!")
            return redirect('task_list')
        except Exception as e:
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
    
    return render(request, "signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not all([username, password]):
            messages.error(request, "Usuario y contraseña son obligatorios")
            return render(request, "registration/login.html")
        
        # Autenticar
        user = authenticate(request, username=username, password=password)
        
        # Si no funciona con username, intentar con email
        if user is None:
            try:
                user_by_email = User.objects.get(email=username)
                user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            messages.success(request, "Sesión iniciada.")
            return redirect('task_list')
        else:
            messages.error(request, "Credenciales inválidas")
    
    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "task_list.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
            messages.success(request, "Tarea añadida.")
    return redirect('task_list')

@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.done = not task.done
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.warning(request, "Tarea eliminada.")
    return redirect('task_list')