# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#IMPORTS PARA DRIVERS CON CASSANDRA

import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine.models import Model



class aulas(Model):
    aula_id = columns.UUID(primary_key=True, required=True)
    nombre = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
    piso = columns.Integer(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
    capacidad = columns.Integer(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
    #dia = columns.Text(required=False)




