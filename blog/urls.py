
from django.contrib import admin
from django.urls import include,path
from blog import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('postComment/',views.postcomment,name='postComment'),
    path('<str:slug>', views.blogPost, name='blogPost'),

]