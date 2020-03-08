# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine.models import Model
# Create your models here.
# class aulas(Model):
#  aula_id = columns.UUID(required=True, primary_key=True)
#  capacidad = columns.Integer(required=False)
#  dia = columns.Text(required=False)
#  #horario = columns.Text(required=False)
#  nombre = columns.Text(required=False)
#  piso =columns.Integer(required=False)
