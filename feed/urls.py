from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.user_posts, name='user_posts'),
    path('logout/', views.logout_user, name='logout'),
]