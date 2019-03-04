from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=128, help_text='Title')
    subtitle = models.CharField(max_length=256, blank=True, help_text='Subtitle')
    label = models.CharField(max_length=256, blank=True, help_text='label')
    date = models.DateField(auto_now_add=True)
    text = RichTextUploadingField(verbose_name='正文')
    blog_like_users = models.ManyToManyField(User, blank=True, related_name='blog_like_users')

    class Meta:
        db_table = 'blog'
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.subtitle}, by {self.author} on {self.date}"


class Profile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    label = models.CharField(max_length=128, default="")
    introduction = models.TextField(max_length=1024, default='')
    header = models.ImageField(upload_to='header', default='header/default.png')
    user_like_blogs = models.ManyToManyField(Blog, blank=True, related_name='user_like_blogs')
    follow_users = models.ManyToManyField(User, blank=True, related_name='follow_users')
    fan_users = models.ManyToManyField(User, blank=True, related_name='fan_users')

    class Meta:
        db_table = 'user_detail_info'
        # ordering = ['-fan_users']


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    text = models.TextField(max_length=512)
    date = models.DateField(auto_now_add=True)
    comment_like_users = models.ManyToManyField(User, blank=True, related_name='comment_like_users')
    reply_comments = models.ManyToManyField('ReplyComment', blank=True, related_name='reply_comments')

    class Meta:
        db_table = 'blog_comment'
        ordering = ['-date']


class ReplyComment(models.Model):
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name='comment_reply')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_comment_user')
    text = models.TextField(max_length=512)
    date = models.DateField(auto_now_add=True)
    reply_comment_like_users = models.ManyToManyField(User, blank=True, related_name='reply_comment_like_users')

    class Meta:
        db_table = 'reply_comment'
        ordering = ['-date']
