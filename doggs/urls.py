from django.urls import path
from . import views


urlpatterns = [
    path('', views.dogs, name='dogs'),
    path('dog/<str:pk>/', views.dog, name='dog'),

    path('create-dog/', views.createDog, name='create-dog'),
    path('update-dog/<str:pk>/', views.updateDog, name='update-dog'),
    path('delete-dog/<str:pk>/', views.deleteDog, name='delete-dog'),
]
