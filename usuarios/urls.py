from django.urls import path
from .views import RegistroUsuarioView, VerificarEmailView, LoginView

urlpatterns = [
    path('registrar/', RegistroUsuarioView.as_view(), name='registrar_usuario'),  # Ruta para registrar usuarios
    path('verificar-email/<int:user_id>/', VerificarEmailView.as_view(), name='verificar_email'),  # Agrega esta línea
    path('login/', LoginView.as_view(), name='login'),  # Ruta de login
]
