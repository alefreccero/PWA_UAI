# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect

from .forms import AulasForm
import uuid
#IMPORTS PARA QUE FUNCIONE EL DRIVER CON CASSANDRA

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
#from models import ExampleModel
from aulas.models import aulas

from django.db import connection
from django.http import HttpResponse 

def crearaulas(nombre,capacidad,piso,dia):
        #agregar un dia y crear las aulas x 5
    aulita = aulas() # Instancio un objeto aula
    aulita.aula_id = uuid.uuid1()
    aulita.nombre = nombre # asigno los valores del form en la prop del objeto instanciado en el paso anterior
    aulita.capacidad= capacidad # asigno los valores del form en la prop del objeto instanciado en el paso anterior
    aulita.piso= piso
    aulita.dia= dia
    aulita.enuso = False
    aulita.save() # salvo el objeto en la DB
    #return HttpResponse("CREASTE UN AULA")


def get_aula(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AulasForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #
            # cursor = connection.cursor()
            # result = cursor.execute("select count (*) FROM aulas WHERE enuso= false ALLOW FILTERING")
            # resultint = int(result[0])
            # todasaulas = aulas.objects.all().filter(capacidad=10)
            #todasaulas = todasaulas.filter(capacidad=10)
            # cuenta = todasaulas.count()
            # redirect to a new URL:
            # if cuenta == 12:
                data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
                aulanombre = data.get('aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
                aulacapa = data.get('capacidad') #esto refiere al nombre que dEfinimos en el form.py
                aulapiso = data.get('piso')
                cluster = Cluster(['127.0.0.1'])
                session = cluster.connect()
                session.set_keyspace('dbpwa')
                query = session.prepare('SELECT * FROM aulas WHERE nombre=? ALLOW FILTERING;')#PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
                rows = session.execute(query, [aulanombre]) #EJECUTO LA QUERY Y LE PASO LAS VARIABLES PARA FILTRAR IMPORTANTE QUE ESTEN ENTRE CORCHETES
                existen = [] #CREO UN ARRAY
                for row in rows:
                    existen.append(row) #LLENO EL ARRAY CON LAS FILAS
                cluster.shutdown() # Cierro La conexion
                if len(existen) > 0: #VERIFICO SI ESE TURNO PARA ESA COMISION YA ESTA USADO
                    return HttpResponse("El aula {} ya existe".format(aulanombre))

                else:
                    #agregar un dia y crear las aulas x 5

                    crearaulas(aulanombre,aulacapa,aulapiso,'Lunes')
                    crearaulas(aulanombre,aulacapa,aulapiso,'Martes')
                    crearaulas(aulanombre,aulacapa,aulapiso,'Miercoles')
                    crearaulas(aulanombre,aulacapa,aulapiso,'Jueves')
                    crearaulas(aulanombre,aulacapa,aulapiso,'Viernes')
                    cluster.shutdown() # Cierro La conexion
                    # aulita = aulas() # Instancio un objeto aula
                    # aulita.aula_id = uuid.uuid1()
                    # aulita.nombre = aulanombre # asigno los valores del form en la prop del objeto instanciado en el paso anterior
                    # aulita.capacidad= aulacapa # asigno los valores del form en la prop del objeto instanciado en el paso anterior
                    # aulita.piso= aulapiso
                    # aulita.enuso = False
                    # aulita.save() # salvo el objeto en la DB
                    # cluster.shutdown() # Cierro La conexion
                    return HttpResponse("CREASTE UN AULA")

        # if a GET (or any other method) we'll create a blank form
    else:

        form = AulasForm()


    return render(request, 'aula.html', {'form': form})

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = AulasForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#              data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
#              aulanombre = data.get('aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
#              aulacapa = data.get('capacidad') #esto refiere al nombre que definimos en el form.py
#              capa = int(aulacapa) #lo fuerzo a int porque nose porque piensa que es un int, sin esta conversion falla el insert
#              cursor = connection.cursor()
#              result = cursor.execute("INSERT INTO aulas(id_aula, capacidad, nombre) VALUES (now(),%s,%s)",(capa, aulanombre)) # refiero los values con el comodin %s luego le clavo las variables
#              return HttpResponse("CREASTE UN AULA!!")
#             #return HttpResponseRedirect('/AULACREADA/')

#     # if a GET (or any other method) we'll create a blank form
#     else:

#         form = AulasForm()


#     return render(request, 'aula.html', {'form': form})


# def get_materias(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = materiasForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#              data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
#              aulanombre = data.get('aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
#              aulacapa = data.get('capacidad') #esto refiere al nombre que definimos en el form.py
#              capa = int(aulacapa) #lo fuerzo a int porque nose porque piensa que es un int, sin esta conversion falla el insert
#              cursor = connection.cursor()
#              result = cursor.execute("INSERT INTO aulas(id_aula, capacidad, nombre) VALUES (now(),%s,%s)",(capa, aulanombre)) # refiero los values con el comodin %s luego le clavo las variables
#              return HttpResponse("CREASTE UN AULA!!")
#             #return HttpResponseRedirect('/AULACREADA/')

#     # if a GET (or any other method) we'll create a blank form
#     else:

#         form = materiasForm()


#     return render(request, 'name.html', {'form': form})




    # def get_name(request):
    # # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = AulasForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #          data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
    #          aulanombre = data.get('aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
    #          aulacapa = data.get('capacidad') #esto refiere al nombre que dEfinimos en el form.py
    #          cluster = Cluster(['127.0.0.1'])
    #          session = cluster.connect()
    #          session.set_keyspace('dbpwa')
    #          insert  = aulas(nombre=aulanombre), aulas(capacidad=aulacapa) 
    #          insert.save()
    #          cluster.shutdown()
    #          return HttpResponse("ENTRO AL IS VALID")
    #         #return HttpResponseRedirect('/thanks/')

    # # if a GET (or any other method) we'll create a blank form
    # else:

    #     form = AulasForm()


    # return render(request, 'name.html', {'form': form})