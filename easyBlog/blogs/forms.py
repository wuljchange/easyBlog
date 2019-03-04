from django import forms
from .models import Blog
# from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='题目')
    subtitle = forms.CharField(max_length=256, label='小标题')
    label = forms.CharField(max_length=256, label='关键字')
    text = forms.CharField(widget=CKEditorUploadingWidget, label='正文')

    class Meta:
        model = Blog
        fields = ['title', 'subtitle', 'label', 'text']