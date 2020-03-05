from django.urls import path

from . import views

urlpatterns = [
    path('planificador', views.reporte_planificador, name='reporte_planificador'),
]