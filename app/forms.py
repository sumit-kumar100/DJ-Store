from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Address, Order


class RegistrationForm(UserCreationForm):
    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': "name@gmail.com",
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-2'
            }),
        label='Email'
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "••••••••",
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-2'
            }),
        label=_('Password')
    )
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "••••••••",
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-2'
            })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'required': True, 'placeholder': "john",
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'
                }),
            'last_name': forms.TextInput(
                attrs={
                    'required': True, 'placeholder': "doe",
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'
                }),
            'username': forms.TextInput(
                attrs={
                    'placeholder': "name@gmail.com",
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'
                }),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': "name@gmail.com",
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'
            }),
        label='Email'
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "••••••••",
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'
            })
    )


# Address Form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'locality', 'state', 'zipcode', 'phone_no']
        widgets = {
            'state': forms.Select(
                attrs={

                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'})
        }


# Checkout form
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(
                attrs={

                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-zinc-200 dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-1 mb-4'}),
        }
