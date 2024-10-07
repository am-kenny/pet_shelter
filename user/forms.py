from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from user.models import UserMedia, CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        error_messages = {
            'email': {
                'unique': 'User with that email already exists.'
            },
            'username': {
                'unique': 'User with that username already exists.'
            }
        }


class UpdateUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]
        error_messages = {
            'email': {
                'unique': 'User with that email already exists.'
            }
        }


class AddUserMedia(ModelForm):
    class Meta:
        model = UserMedia
        fields = ["media"]
        labels = {
            'media': 'Image upload',
        }
