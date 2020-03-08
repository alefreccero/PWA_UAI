# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine.models import Model


class planificacion(Model):
   read_repair_chance = 0.05 # optional - defaults to 0.1
   planificacion_id = columns.UUID(primary_key=True, default=uuid.uuid4) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
   nombremat = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
   comision = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
   carrera = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
   aula = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
   turno = columns.Text(required=False)
   piso = columns.Integer(required=False)
   dia= columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS

