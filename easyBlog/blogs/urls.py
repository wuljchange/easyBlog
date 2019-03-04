from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('reply_comment/<int:blog_comment_id>/', views.reply_comment, name='reply_comment'),
    path('search/', views.search, name='search'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('create/', views.create, name='create'),
    path('like_blogs/', views.profile_like_blogs, name='like_blogs'),
    path('follow_users/', views.profile_follow_users, name='follow_users'),
    path('fan_users/', views.profile_fan_users, name='fan_users'),
    path('add_blog/', views.add_like_blog, name='add_like_blog'),
    path('add_fan_users/', views.add_fan_and_follow_users, name='add_fan_users'),
    path('view_other_profile/<int:user_id>/', views.view_other_profile, name='view_other_profile'),
    path('vote_blog_comment/', views.vote_blog_comment, name="vote_blog_comment"),
    path('vote_reply_comment/', views.vote_reply_comment, name="vote_reply_comment"),
    path('delete_blog/<int:blog_id>', views.delete_blog, name="delete_blog"),
    # path('delete/', views.delete_users, name='delete')
]