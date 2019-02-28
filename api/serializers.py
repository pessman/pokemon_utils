from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists, get_username_max_length
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(
        required=allauth_account_settings.EMAIL_REQUIRED
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this email address."
                )
        return email

    def validate_password1(self, password):
        password = get_adapter().clean_password(password)
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                "The two passwords fields didn't match."
            )
        return data

    def get_cleaned_data(self):
        data = {
            'username': self.validated_data.get('username'),
            'password1': self.validated_data.get('password1'),
            'email': self.validated_data.get('email')
        }
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user
