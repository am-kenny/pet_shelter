from django.forms import ModelForm
from django.contrib.auth.models import User


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]