from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import timedelta
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer,
    PasswordChangeSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    EmailVerificationSerializer
)
from .models import EmailVerification, PasswordReset

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        token = get_random_string(64)
        expiry_date = timezone.now() + timedelta(days=1)
        EmailVerification.objects.create(user=user, token=token, expires_at=expiry_date)


        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        send_mail(
            'Verify your email on ResearchHub',
            f'Please click the link below to verify your email address:\n{verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'message': 'User created successfully. Please verify your email.',
            'user': UserSerializer(user, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def request_password_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                token = get_random_string(64)
                expiry_date = timezone.now() + timedelta(hours=24)

                PasswordReset.objects.create(
                    user=user,
                    token=token,
                    expires_at=expiry_date
                )

                reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
                send_mail(
                    'Reset your password on ResearchHub',
                    f'Please click the link below to reset your password:\n{reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:

                return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def confirm_password_reset(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']

            try:
                reset_request = PasswordReset.objects.get(
                    token=token,
                    expires_at__gt=timezone.now(),
                    is_used=False
                )

                user = reset_request.user
                user.set_password(serializer.validated_data['new_password'])
                user.save()


                reset_request.is_used = True
                reset_request.save()

                return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
            except PasswordReset.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify_email(self, request):
        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']

            try:
                verification = EmailVerification.objects.get(
                    token=token,
                    expires_at__gt=timezone.now()
                )

                user = verification.user
                user.is_email_verified = True
                user.save()


                verification.delete()

                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            except EmailVerification.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resend_verification(self, request):
        user = request.user

        if user.is_email_verified:
            return Response({'message': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)


        EmailVerification.objects.filter(user=user).delete()


        token = get_random_string(64)
        expiry_date = timezone.now() + timedelta(days=1)
        EmailVerification.objects.create(user=user, token=token, expires_at=expiry_date)


        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        send_mail(
            'Verify your email on ResearchHub',
            f'Please click the link below to verify your email address:\n{verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Verification email sent'}, status=status.HTTP_200_OK)