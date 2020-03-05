# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#IMPORTS PARA DRIVERS CON CASSANDRA

import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine.models import Model


# A BORRAR QUEDA POR SI FALLA EL CAMBIO DE NOMBRES
# class ExampleModel(Model):
#  read_repair_chance = 0.05 # optional - defaults to 0.1
#  example_id = columns.UUID(primary_key=True, default=uuid.uuid4)
#  id_aula = columns.TIMEUUID(default=uuid.uuid4)
#  description = columns.Text(required=False)

class aulas(Model):
    aula_id = columns.UUID(primary_key=True, required=True)
    nombre = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
    piso = columns.Integer(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
    capacidad = columns.Integer(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
    dia = columns.Text(required=False)

# class materias(Model):
#  read_repair_chance = 0.05 # optional - defaults to 0.1
#  id_materia = columns.UUID(primary_key=True, default=uuid.uuid4) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
#  nombremat = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
#  carrera = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
#  turno = columns.Text(required=False)
#  horario = columns.Text(required=False)
#  comision = columns.Text(required=False)
#  CantAlumnos =columns.Integer(required=False)


