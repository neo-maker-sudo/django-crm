from django import forms
from base.models import User


class AgentForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs={
                "id": "username", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': "John Cena"
            }
        ),
    )

    email = forms.CharField(
        required=True,
        widget = forms.EmailInput(
            attrs={
                "id": "email", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': "example@gmail.com"
            }
        ),
    )

    first_name = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs={
                "id": "first_name", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': "John"
            }
        ),
    )

    last_name = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs={
                "id": "last_name", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': "Cena"
            }
        ),
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name',]
    
    
    def __init__(self, **kwargs):
        agent = kwargs.get("instance")
        super().__init__(**kwargs)

        if agent:        
            self.fields["username"].initial = agent.user.username
            self.fields["email"].initial = agent.user.email
            self.fields["first_name"].initial = agent.user.first_name
            self.fields["last_name"].initial = agent.user.last_name