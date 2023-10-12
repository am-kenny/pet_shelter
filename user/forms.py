from django.forms import ModelForm, BooleanField, HiddenInput
from django.contrib.auth.models import User

from user.models import UserMedia


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class AddUserMedia(ModelForm):

    class Meta:
        model = UserMedia
        fields = ["media"]
        labels = {
            'media': 'Image upload',
        }
