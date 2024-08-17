from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/detail/<blog_id>', views.details, name='details'),
    path('blog/pub', views.publish, name='publish'),
    path('blog/comment/pub', views.pub_comment, name='comment'),
    path('search', views.search, name='search')
]