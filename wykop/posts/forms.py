from django.forms.models import ModelForm

from wykop.posts.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']