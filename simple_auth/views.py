from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(generics.CreateAPIView):
    """
    Creates new user and returns an authentication token.
    """
    serializer_class = RegistrationSerializer


class LoginView(generics.CreateAPIView):
    """
    Authenticate user in order to obtain token.
    Additionally returns datetimes of previous entries.
    """
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
