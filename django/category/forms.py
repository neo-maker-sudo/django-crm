from dataclasses import fields
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs={
                "id": "name", 
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': "Category name"
            }
        ),
    )

    class Meta:
        model = Category
        fields = ("name",)
