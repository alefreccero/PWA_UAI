# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine.models import Model

class cursadas(Model):
 nombremat = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
 carrera = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
 turno = columns.Text(required=False)
 #horario = columns.Text(required=False)
 comision = columns.Text(required=False)
 cantalumnos =columns.Integer(required=False)
 cursada_id = columns.UUID(required=True, primary_key=True)

