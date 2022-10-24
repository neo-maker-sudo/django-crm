from django.contrib.auth.forms import (
    UserCreationForm, UsernameField, PasswordResetForm, SetPasswordForm,
    AuthenticationForm
)
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from base.models import User


class LoginForm(AuthenticationForm):
    
    def __init__(self, request, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                "id": "username", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )

        self.fields['password'].widget.attrs.update(
            {
                "id": "password", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            try:
                if self.user_cache is None:
                    error = self.get_invalid_login_error()
                    return self.add_error("username", error)

                self.confirm_login_allowed(self.user_cache)

            except ValidationError as error:
                return self.add_error("username", error)

        return self.cleaned_data

class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                "id": "username", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )

        self.fields['password1'].widget.attrs.update(
            {
                "id": "password1", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )

        self.fields['password2'].widget.attrs.update(
            {
                "id": "password2", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update(
            {
                "id": "email", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': "example@gmail.com"
            }
        )


class CustomPasswordConfirmForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

        self.fields['new_password1'].widget.attrs.update(
            {
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )
        self.fields['new_password2'].widget.attrs.update(
            {
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',             }
        )
