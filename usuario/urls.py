from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import RedirectAuthenticatedLoginView

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', RedirectAuthenticatedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name = 'registrar-usuario'),  
    path('listar/', views.listarUsuarios, name = 'listar-usuarios'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name = 'password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'), #recebe a informação do email para receber token e liberar alteração
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'), 
    path('perfil/', views.perfilUser, name='perfil_usuario'),
    path('listarAdmMaster/', views.listarAdmMaster, name='listarAdmMaster'),
    path('removerAdmMaster/<int:id_adm>', views.removerAdmMaster, name='removerAdmMaster'),
    path('promover/', views.promoverAdmMaster, name='promoverAdmMaster'),
    path('perfil/editar/', views.editarPerfilUser, name='editar_perfil_usuario'),
    path('detalharUsuario/<str:matricula>/', views.detalharUsuario, name = 'detalhar-usuario'),
    # path('', include('django.contrib.auth.urls'))

] 

