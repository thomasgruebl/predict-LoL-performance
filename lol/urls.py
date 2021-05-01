from django.urls import path

from . import views

urlpatterns = [
    # lol app home page
    path('', views.index, name='index'),
    # lol app about page
    path('about/', views.about, name='about')
]