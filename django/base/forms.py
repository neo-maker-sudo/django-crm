from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UsernameField, PasswordResetForm, SetPasswordForm,
    AuthenticationForm
)
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
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


class CustomPasswordChangeForm(SetPasswordForm):

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        "old_password_incorrect": _("old password incorrect, please enter again."),
        "password_match_error": _("old password could not be same as new password, please enter again."),
    }

    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'old-password'}),
        strip=False,
    )

    field_order = ['old_password', 'new_password1', 'new_password2',]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

        self.fields['old_password'].widget.attrs.update(
            {
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )

        self.fields['new_password1'].widget.attrs.update(
            {
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            }
        )
        self.fields['new_password2'].widget.attrs.update(
            {
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',             }
        )

    def clean(self):
        cleaned_data = super().clean()
          
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        
        if not self.user.check_password(old_password):
            error = ValidationError(
                self.error_messages["old_password_incorrect"],
                code="old_password_incorrect"
            )
            self.add_error("old_password", error)
        
        if old_password == new_password1:
            error = ValidationError(
                self.error_messages["password_match_error"],
                code="password_match_error"
            )
            self.add_error("new_password1", error)
        
        return cleaned_data

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
