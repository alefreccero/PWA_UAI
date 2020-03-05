from django.urls import path

from . import views

urlpatterns = [
    path('', views.reporte4, name='reporte4'),
]