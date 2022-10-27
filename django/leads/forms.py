from django import forms
from django.core.validators import FileExtensionValidator
from .models import Lead
from agents.models import Agent
from base.models import Organization
from category.models import Category


class ForeignKeyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.user.username


class LeadForm(forms.ModelForm):
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

    age = forms.IntegerField(
        required=True,
        widget = forms.NumberInput(
            attrs={
                "id": "age", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': 0
            }
        ),
    )

    description = forms.CharField(
        widget = forms.Textarea(
            attrs={
                "id": "description",
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "Enter yourself information"
            }
        )
    )
    
    email = forms.EmailField(
        widget= forms.EmailInput(
            attrs={
                "id": "email",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "exmaple@gmail.com"
            }
        )
    )
    
    phone_number = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "id": "phone_number",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        )
    )
    
    avatar = forms.ImageField(
        widget = forms.FileInput(
            attrs={
                "id": "avatar",
                "class": "form-control bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "accept": ".png, .jpg, .webp"
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["png", "jpg", "webp"],
                message="not allow %(extension)s, only accept %(allowed_extrnsions)s format"
            )
        ]
    )
    
    # https://flowbite.com/docs/forms/select/
    agent = forms.ModelChoiceField(
        required=False,
        queryset=Agent.objects.all(),
        widget= forms.Select(attrs={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
    )

    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget= forms.Select(attrs={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
    )

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget= forms.Select(attrs={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
    )

    class Meta:
        model = Lead
        fields = [
            "first_name", 
            "last_name", 
            "age", 
            "agent",
            "description", 
            "email",
            "phone_number",
            "avatar",
            "organization", 
            "category"
        ]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        
        
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(
        queryset=Agent.objects.none(),
        widget= forms.Select(attrs={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
    )
    
    def __init__(self, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.organization)
        super().__init__(**kwargs)
        self.fields["agent"].queryset = agents