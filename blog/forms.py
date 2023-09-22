from django.forms import ModelForm
from blog.models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["title", "text", "media", "animal"]
