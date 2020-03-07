from django.urls import path

from . import views

urlpatterns = [
    path('', views.showreport1, name='showreport1'),
]