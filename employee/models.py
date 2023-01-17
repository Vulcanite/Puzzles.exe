import datetime as dt
from django.db import models
from user_auth.models import customuser

# Create your models here.
TAGS = (
    ('Self repair', 'Self Repair'),
    ('Request Technician', 'Request Technician')
)

STATUS_LIST = (
    ('OPENED', 'OPENED'),
    ('APPROVED', 'APPROVED'),
    ('REJECTED', 'REJECTED')
)

status_list = ["OPENED", "APPROVED", "REJECTED"]

class RequestTable(models.Model):
    title = models.CharField(max_length=150)
    request_tags = models.CharField(choices=TAGS, max_length=50, default='Request Technician')
    description = models.CharField(max_length=250)
    last_update = models.DateTimeField(default=dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30), blank=True)
    status =  models.CharField(choices=STATUS_LIST, max_length=50, default='OPENED')
    created_by = models.ForeignKey(customuser, on_delete=models.CASCADE, blank = True, null = True)
