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
    
    cursadarows = cursadas.objects.all()
    allcursadas = []
    for row in cursadarows:
        allcursadas.append(row)

    cluster.shutdown()

    aulas_ordenadas=sorted(allaulas,key=lambda aulas:aulas.capacidad)
    cursadas_ordenadas=sorted(allcursadas,key=lambda cursadas:cursadas.cantalumnos,reverse=True)
    
    asignar(aulas_ordenadas,cursadas_ordenadas)
   
    # return HttpResponse('OK')
    return HttpResponseRedirect("http://127.0.0.1:8000/reportes/planificador")


def asignar(laulas,lcursadas):
    for dia in ['Lunes','Martes','Miercoles','Jueves','Viernes']:
        for aula in laulas:
            for turno in ['Manana','Tarde','Noche']:
                if len(lcursadas)>0:
                    seuso=False
                    for cursada in lcursadas:
                        if aula.capacidad>=cursada.cantalumnos and cursada.turno==turno:
                            cluster = Cluster(['127.0.0.1'])
                            session = cluster.connect()
                            session.set_keyspace('dbpwa')
                            query=session.prepare('SELECT * FROM planificacion WHERE carrera=? AND comision=? AND turno=? AND dia=? ALLOW FILTERING;')
                            queryejecutada=session.execute(query,[cursada.carrera,cursada.comision,cursada.turno,dia])
                            auxiliar = []
                            for row in queryejecutada:
                                auxiliar.append(row)
                            cluster.shutdown()
                            if len(auxiliar)==0:
                                #INICIO DE LOGICA DE INSERCION EN DB
                                cluster = Cluster(['127.0.0.1'])
                                session = cluster.connect()
                                session.set_keyspace('dbpwa')
                                session.execute("INSERT INTO planificacion(planificacion_id, carrera, nombremat, comision, turno, aula, piso, dia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursada.carrera, cursada.nombremat, cursada.comision, cursada.turno, aula.nombre, aula.piso,dia))
                                cluster.shutdown()
                                #FIN DE LOGICA DE INSERCION EN DB
                                lcursadas.remove(cursada)
                                seuso=True
                                break
                    if seuso==False:
                        #INICIO DE LOGICA DE INSERCION EN DB
                        cluster = Cluster(['127.0.0.1'])
                        session = cluster.connect()
                        session.set_keyspace('dbpwa')
                        session.execute("INSERT INTO aulasinuso(aulasinuso_id, nombre, capacidad, piso, turno, dia) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), aula.nombre, aula.capacidad, aula.piso, turno, dia))
                        cluster.shutdown()
                        #FIN DE LOGICA DE INSERCION EN DB 
                else:
                    #INICIO DE LOGICA DE INSERCION EN DB
                    cluster = Cluster(['127.0.0.1'])
                    session = cluster.connect()
                    session.set_keyspace('dbpwa')
                    session.execute("INSERT INTO aulasinuso(aulasinuso_id, nombre, capacidad, piso, turno, dia) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), aula.nombre, aula.capacidad, aula.piso, turno, dia))
                    cluster.shutdown()
                    #FIN DE LOGICA DE INSERCION EN DB 
    if len(lcursadas)>0:
        for cursada in lcursadas:
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            session.execute("INSERT INTO cursadasinaula(cursadasinaula_id, carrera, nombremat, cantalumnos, comision, turno) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursada.carrera, cursada.nombremat,cursada.cantalumnos, cursada.comision, cursada.turno))
            cluster.shutdown()                      

