from django.db import models

# Create your models here.
TAGS = (
    ('Self repair', 'Self Repair'),
    ('Request Technician', 'Request Technician')
)

class RequestTable(models.Model):
    title = models.CharField(max_length=150)
    request_tags = models.CharField(choices=TAGS, max_length=50, default='Request Technician')
    description = models.CharField(max_length=250)
    last_update = models.DateTimeField(auto_now_add=True)
    