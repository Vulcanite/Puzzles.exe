from contextlib import nullcontext
from django.db import models

class hardware_details(models.Model):
    emp_pc_config = models.JSONField()
    emp_ip_address = models.CharField(max_length=100, unique=True)
    emp_name = models.CharField(max_length = 100, unique=True, null=True, default=None)