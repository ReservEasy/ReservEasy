from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
# app_name = "conta"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), 
    path('register/', views.register, name = 'registrar-usuario'),  
    path('listar/', views.listarUsuarios, name = 'listar-usuarios')  
]