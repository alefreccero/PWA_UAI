from django.urls import path

from . import views

urlpatterns = [
    path('', views.reporte5, name='reporte5'),
]