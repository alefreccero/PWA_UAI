"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^aulas/', include('aulas.urls')),
    url(r'^aula/', include('aulas.urls')),
    url(r'^cursadas/', include('cursadas.urls')),
    url(r'^cursada/', include('cursadas.urls')),
    url(r'^ReporteCursada_libre/', include('reporte1.urls')),
    url(r'^reportecursada_libre/', include('reporte1.urls')),
    url(r'^planificador/', include('asignador.urls')),
    url(r'^reportes/', include('reporte2.urls')),
    url(r'^ReporteAula/', include('reporte4.urls')),
    url(r'^reporteaula/', include('reporte4.urls')),
    url(r'^ReporteAula_libre/', include('reporte3.urls')),
    url(r'^reporteaula_libre/', include('reporte3.urls')),
    url(r'^ReporteComision/', include('reporte5.urls')),
    url(r'^reportecomision/', include('reporte5.urls')),
    url(r'^admin/', admin.site.urls)

]
