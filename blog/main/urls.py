from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('registration', views.registration, name='registration'),
    path('home', views.home, name='home'),
    path('loggout', views.loggout, name='loggout'),
    path('blog', views.blog, name='blog'),
    path('profile', views.profile, name='profile'),
    path('addpost', views.add_post, name='addpost'),
    path('delete/<_id>/', views.deletepost, name='delete'),
    path('comment/<_id>/', views.addcomment, name='comment'),
    path('edit/<_id>/', views.edit, name='edit'),
]
