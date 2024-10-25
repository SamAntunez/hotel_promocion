from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistroUsuarioSerializer
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Usuario  # Importa el modelo de usuario personalizado
from django.contrib.auth import authenticate

class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            try:
                enviar_correo_verificacion(usuario)
                return Response(
                    {"message": "Registro exitoso. Revisa tu correo electrónico para verificar tu cuenta."}, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"message": "Usuario creado, pero no se pudo enviar el correo de verificación. Error: {}".format(e)}, 
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')  # Cambiar a username
        password = request.data.get('password')

        # Autenticar al usuario con nombre de usuario y contraseña
        usuario = authenticate(request, username=username, password=password)

        if usuario:
            if usuario.is_active:
                return Response({"message": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
            return Response({"message": "Cuenta no verificada o inactiva"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)

def enviar_correo_verificacion(usuario):
    url_verificacion = reverse('verificar_email', args=[usuario.id])
    link = f"http://localhost:8000{url_verificacion}" # Asegúrate de que el dominio sea correcto
    subject = "Verificación de correo electrónico"
    message = f"Hola {usuario.username}, por favor verifica tu correo haciendo clic en el siguiente enlace: {link}"
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        fail_silently=False,
    )

class VerificarEmailView(APIView):
    def get(self, request, user_id):
        try:
            usuario = Usuario.objects.get(id=user_id)
            if usuario.email_verificado:
                return Response({"message": "El correo ya está verificado."}, status=status.HTTP_400_BAD_REQUEST)

            # Marcar el email como verificado
            usuario.email_verificado = True
            usuario.is_active = True  # Habilitar al usuario tras verificar el email
            usuario.save()
            return Response({"message": "Correo verificado exitosamente."}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({"message": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
