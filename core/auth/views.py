from rest_framework import status
from rest_framework.response import Response
from blog.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        refresh = RefreshToken.for_user(user)
        data = {
            'email': user.email,
            'access_token': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)