from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticación
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Tareas
    path("", views.task_list, name="task_list"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:pk>/toggle/", views.toggle_task, name="toggle_task"),
    path("tasks/<int:pk>/delete/", views.delete_task, name="delete_task"),
]
