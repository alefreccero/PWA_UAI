# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine.models import Model
# Create your models here.
class aulas(Model):
 read_repair_chance = 0.05 # optional - defaults to 0.1
 id_aula = columns.UUID(primary_key=True, default=uuid.uuid4) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
 nombre = columns.Text(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS
 capacidad = columns.Integer(required=False) #ESTOS NOMBRES COPIAN LOS NOMBRES DE LAS COLUMNAS EN LAS TABLAS