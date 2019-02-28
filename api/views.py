from allauth.account import app_settings as allauth_account_settings
from allauth.account.utils import complete_signup
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from api.serializers import RegistrationSerializer

sensitive_post_params = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = ()
    authentication_classes = ()

    @sensitive_post_params
    def dispatch(self, *args, **kwargs):
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def get_response_data(self, data):
        if allauth_account_settings.EMAIL_VERIFICATION == \
                allauth_account_settings.EmailVerificationMethod.MANDATORY:
            return {
                "detail": "Verification email sent."
            }
        data = {
            "username": data.get('username'),
            "password": data.get('password1')
        }
        try:
            return TokenObtainPairSerializer().validate(data)
        except TokenError as e:
            raise InvalidToken(e.args[0])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_response_data(serializer.cleaned_data),
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        # try:
        #     self.token = TokenObtainPairSerializer.is_valid(raise_exception=True)
        # except TokenError as e:
        #     raise InvalidToken(e.args[0])
        complete_signup(self.request._request, user,
                        allauth_account_settings.EMAIL_VERIFICATION, None)
        return user
