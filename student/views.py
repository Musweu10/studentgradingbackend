from .serializers import AttendanceSerializer
from teacher.models import Attendance
from rest_framework import generics
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import (
    StudentRegistrationSerializer,
    LoginSerializer,
    StudentProfileSerializer
)

User = get_user_model()

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = CommuterRegistrationSerializer
#     permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the new user

        # Generate JWT tokens for the newly registered user
        refresh = RefreshToken.for_user(user)

        # Prepare the response with user details and tokens
        response_data = {
            'id': str(user.id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'guardian_first_name': user.guardian_first_name,
            'guardian_last_name': user.guardian_last_name,
            'guardian_phone_number': user.guardian_phone_number,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # Allow public access for login
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data  # User object from the serializer

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)

        # Return user details along with tokens
        return Response({
            'id': str(user.id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'guardian_first_name': user.guardian_first_name,
            'guardian_last_name': user.guardian_last_name,
            'guardian_phone_number': user.guardian_phone_number,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


# class LogoutView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         try:
#             token = RefreshToken(request.data.get('refresh'))
#             token.blacklist()  # This may raise an exception if token is invalid
#             return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             print(e)  # Debug the exception to see what's going wrong
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token if the blacklist app is installed
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Handle exceptions, e.g., if the token is invalid or expired
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(student=user).order_by('-date')
