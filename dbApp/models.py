from django.db import models
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
 
# Create your models here.

class ExampleModel(Model):
    read_repair_chance = 0.05 # optional - defaults to 0.1
    example_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    description = columns.Text(required=False)