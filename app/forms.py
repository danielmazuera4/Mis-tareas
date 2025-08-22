from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Task

class SignupForm(UserCreationForm):
    # pedimos email y lo volvemos único + minúsculas
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ese correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class EmailOrUsernameAuthenticationForm(forms.Form):
    # permite iniciar con usuario O email
    username_or_email = forms.CharField(label="Usuario o correo")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self):
        cleaned = super().clean()
        uoe = cleaned.get("username_or_email", "").strip()
        password = cleaned.get("password")

        # Intentar autenticar por username
        user = authenticate(username=uoe, password=password)
        if not user:
            # Intentar por email -> mapear email a username
            try:
                user_obj = User.objects.get(email__iexact=uoe)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if not user:
            raise forms.ValidationError("Credenciales inválidas.")
        cleaned["user"] = user
        return cleaned


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Nueva tarea…"})
        }
        labels = {"title": ""}
