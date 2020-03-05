# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
import uuid
from asignador.forms import cursadasForm

#IMPORTS PARA QUE FUNCIONE EL DRIVER CON CASSANDRA

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from cursadas.models import cursadas
from aulas.models import aulas
#from django.db import connection
from django.http import HttpResponse 
from cassandra.cqlengine import columns
from collections import namedtuple


def lista(vv):
    for v in vv:
        print(v)

def get_asignador(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = cursadasForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            session.execute("truncate dbpwa.planificacion")
            session.execute("truncate dbpwa.aulasinuso")
            session.execute("truncate dbpwa.cursadasinaula")
            #cluster.shutdown()
                         
            aularows = aulas.objects.all()
            allaulas = []
            for row in aularows:
               allaulas.append(row)

            cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Manana' ALLOW FILTERING;")
            cursadas_manana = []
            for row in cursadarows:
                cursadas_manana.append(row)
            
            cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Tarde' ALLOW FILTERING;")
            cursadas_tarde = []
            for row in cursadarows:
               cursadas_tarde.append(row)
     
            cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Noche' ALLOW FILTERING;")
            cursadas_noche = []
            for row in cursadarows:
               cursadas_noche.append(row)

            cluster.shutdown()

            aulas_ordenadas=sorted(allaulas,key=lambda aulas:aulas.capacidad)
            manana_ordenadas=sorted(cursadas_manana,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
            tarde_ordenadas=sorted(cursadas_tarde,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
            noche_ordenadas=sorted(cursadas_noche,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
            
            
            ordenar(aulas_ordenadas,manana_ordenadas, 'Manana')
            
            ordenar(aulas_ordenadas,tarde_ordenadas,'Tarde')
            
            ordenar(aulas_ordenadas,noche_ordenadas,'Noche')
            
            return HttpResponse('OK')

    # if a GET (or any other method) we'll create a blank form
    else:

        form = cursadasForm()


    return render(request, 'asignador.html', {'form': form})


def ordenar(lista_aulas,lista_cursadas,turno): #defino la funcion
    aulas_ordenadas=lista_aulas #asigno la lista que me pasan como parametro a una variable
    cursadas_ordenadas=lista_cursadas #asigno la lista que me pasan como parametro a una variable

    for x in range(len(aulas_ordenadas)):        
        if len(cursadas_ordenadas)>0:
            aula_usada=False
            for y in range(len(cursadas_ordenadas)):
                if aulas_ordenadas[x].capacidad>=cursadas_ordenadas[y].cantalumnos:
                    print('aula nro:',aulas_ordenadas[x].nombre,'cursada:',cursadas_ordenadas[y].nombremat)
                    #INICIO DE LOGICA DE INSERCION EN DB
                    cluster = Cluster(['127.0.0.1'])
                    session = cluster.connect()
                    session.set_keyspace('dbpwa')
                    session.execute("INSERT INTO planificacion(planificacion_id, carrera, nombremat, comision, turno, aula, piso, dia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursadas_ordenadas[y].carrera, cursadas_ordenadas[y].nombremat, cursadas_ordenadas[y].comision, cursadas_ordenadas[y].turno, aulas_ordenadas[x].nombre, aulas_ordenadas[x].piso,aulas_ordenadas[x].dia))
                    cluster.shutdown()
                    #FIN DE LOGICA DE INSERCION EN DB

                    cursadas_ordenadas.pop(y)
                    aula_usada=True
                    break
            if aula_usada==False:
                print('AULA SIN USAR:',aulas_ordenadas[x].nombre)
                #INICIO DE LOGICA DE INSERCION EN DB
                cluster = Cluster(['127.0.0.1'])
                session = cluster.connect()
                session.set_keyspace('dbpwa')
                session.execute("INSERT INTO aulasinuso(aulasinuso_id, nombre, capacidad, piso, turno, dia) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), aulas_ordenadas[x].nombre, aulas_ordenadas[x].capacidad, aulas_ordenadas[x].piso, turno, aulas_ordenadas[x].dia))
                cluster.shutdown()
                #FIN DE LOGICA DE INSERCION EN DB
                                            
    if len(cursadas_ordenadas)>0:
        print('MATERIA SIN AULA:')
        for z in range(len(cursadas_ordenadas)):
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            session.execute("INSERT INTO cursadasinaula(cursadasinaula_id, carrera, nombremat, cantalumnos, comision, turno) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursadas_ordenadas[z].carrera, cursadas_ordenadas[z].nombremat,cursadas_ordenadas[z].cantalumnos, cursadas_ordenadas[z].comision, cursadas_ordenadas[z].turno))
            cluster.shutdown() 



 