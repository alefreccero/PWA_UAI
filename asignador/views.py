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

    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('dbpwa')
    session.execute("truncate dbpwa.planificacion")
    session.execute("truncate dbpwa.aulasinuso")
    session.execute("truncate dbpwa.cursadasinaula")
                    
    aularows = aulas.objects.all()
    allaulas = []
    for row in aularows:
        allaulas.append(row)

    cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Manana' AND comision='A' ALLOW FILTERING;")
    cursadas_manana_a = []
    for row in cursadarows:
        cursadas_manana_a.append(row)
    
    cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Manana' AND comision='B' ALLOW FILTERING;")
    cursadas_manana_b = []
    for row in cursadarows:
        cursadas_manana_b.append(row)

    cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Tarde' AND comision='A' ALLOW FILTERING;")
    cursadas_tarde_a= []
    for row in cursadarows:
        cursadas_tarde_a.append(row)
    
    cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Tarde' AND comision='B' ALLOW FILTERING;")
    cursadas_tarde_b = []
    for row in cursadarows:
        cursadas_tarde_b.append(row)

    cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Noche' AND comision='A' ALLOW FILTERING;")
    cursadas_noche_a = []
    for row in cursadarows:
        cursadas_noche_a.append(row)

    cursadarows = session.execute("SELECT * FROM cursadas WHERE turno='Noche' AND comision='B' ALLOW FILTERING;")
    cursadas_noche_b = []
    for row in cursadarows:
        cursadas_noche_b.append(row)

    cluster.shutdown()

    aulas_ordenadas=sorted(allaulas,key=lambda aulas:aulas.capacidad)
    manana_ordenadas_a=sorted(cursadas_manana_a,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    tarde_ordenadas_a=sorted(cursadas_tarde_a,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    noche_ordenadas_a=sorted(cursadas_noche_a,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    manana_ordenadas_b=sorted(cursadas_manana_b,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    tarde_ordenadas_b=sorted(cursadas_tarde_b,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    noche_ordenadas_b=sorted(cursadas_noche_b,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    
    
    ordenar(aulas_ordenadas,manana_ordenadas_a,manana_ordenadas_b,'Manana')
    ordenar(aulas_ordenadas,tarde_ordenadas_a,tarde_ordenadas_b,'Tarde')
    ordenar(aulas_ordenadas,noche_ordenadas_a,noche_ordenadas_b,'Noche')
    
    # return HttpResponse('OK')
    return HttpResponseRedirect("http://127.0.0.1:8000/reportes/planificador")




def ordenar(lista_aulas,lista_cursadasA,lista_cursadasB,turno): #defino la funcion
    aulas=lista_aulas #asigno la lista que me pasan como parametro a una variable
    cursada_a=lista_cursadasA #asigno la lista que me pasan como parametro a una variable
    cursada_b=lista_cursadasB

    for dia in ['Lunes','Martes','Miercoles','Jueves','Viernes']:
        a=False
        b=False
        if len(cursada_a)>0:
            a=True
        if len(cursada_b)>0:
            b=True
        for x in range(len(aulas)):
            aula_usada=False
            if a==True:
                for y in range(len(cursada_a)):
                   if aulas[x].capacidad>=cursada_a[y].cantalumnos: 
                    #INICIO DE LOGICA DE INSERCION EN DB
                    cluster = Cluster(['127.0.0.1'])
                    session = cluster.connect()
                    session.set_keyspace('dbpwa')
                    session.execute("INSERT INTO planificacion(planificacion_id, carrera, nombremat, comision, turno, aula, piso, dia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursada_a[y].carrera, cursada_a[y].nombremat, cursada_a[y].comision, cursada_a[y].turno, aulas[x].nombre, aulas[x].piso,dia))
                    cluster.shutdown()
                    #FIN DE LOGICA DE INSERCION EN DB
                    cursada_a.pop(y)
                    a=False
                    aula_usada=True
                    break
            if b==True:
                for y in range(len(cursada_b)):
                   if aulas[x].capacidad>=cursada_b[y].cantalumnos: 
                    #INICIO DE LOGICA DE INSERCION EN DB
                    cluster = Cluster(['127.0.0.1'])
                    session = cluster.connect()
                    session.set_keyspace('dbpwa')
                    session.execute("INSERT INTO planificacion(planificacion_id, carrera, nombremat, comision, turno, aula, piso, dia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursada_b[y].carrera, cursada_b[y].nombremat, cursada_b[y].comision, cursada_b[y].turno, aulas[x].nombre, aulas[x].piso,dia))
                    cluster.shutdown()
                    #FIN DE LOGICA DE INSERCION EN DB
                    cursada_b.pop(y)
                    b=False
                    aula_usada=True
                    break
            if aula_usada==False:
                print('AULA SIN USAR:',aulas[x].nombre)
                #INICIO DE LOGICA DE INSERCION EN DB
                cluster = Cluster(['127.0.0.1'])
                session = cluster.connect()
                session.set_keyspace('dbpwa')
                session.execute("INSERT INTO aulasinuso(aulasinuso_id, nombre, capacidad, piso, turno, dia) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), aulas[x].nombre, aulas[x].capacidad, aulas[x].piso, turno, dia))
                cluster.shutdown()
                #FIN DE LOGICA DE INSERCION EN DB    
    if len(cursada_a)>0:
        for z in range(len(cursada_a)):
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            session.execute("INSERT INTO cursadasinaula(cursadasinaula_id, carrera, nombremat, cantalumnos, comision, turno) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursada_a[z].carrera, cursada_a[z].nombremat,cursada_a[z].cantalumnos, cursada_a[z].comision, cursada_a[z].turno))
            cluster.shutdown() 
    if len(cursada_b)>0:
        for z in range(len(cursada_b)):
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            session.execute("INSERT INTO cursadasinaula(cursadasinaula_id, carrera, nombremat, cantalumnos, comision, turno) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursada_b[z].carrera, cursada_b[z].nombremat,cursada_b[z].cantalumnos, cursada_b[z].comision, cursada_b[z].turno))
            cluster.shutdown() 




"""     for x in range(len(aulas_ordenadas)):        
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
            cluster.shutdown()  """



 