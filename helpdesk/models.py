from django.db import models

class hardware_details(models.Model):
    emp_fname = models.CharField(max_length=100)
    emp_pc_config = models.JSONField()
    emp_ip_address = models.CharField(max_length=100)