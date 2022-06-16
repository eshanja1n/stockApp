from django import forms
from post.models import Post

class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['ticker', 'buyDate', 'sellDate', 'caption']
