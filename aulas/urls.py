from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_aula, name='get_aula'),
]