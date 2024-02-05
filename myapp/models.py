# models.py
from django.db import models
from django.utils import timezone

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(null=True, blank=True)
    advisory_type = models.CharField(max_length=255)
    advisory_number = models.CharField(max_length=255)
    advisory_name = models.CharField(max_length=255)
    tenant = models.CharField(max_length=255, default='')
    iocs_matched = models.IntegerField(default=0)
    iocs_list = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.advisory_name



class EmailCredentials(models.Model):
    tenant = models.CharField(max_length=255)
    to = models.TextField(max_length=255)  # Assuming multiple email addresses are comma-separated
    cc = models.TextField(max_length=255)  # Assuming multiple email addresses are comma-separated
    subject = models.CharField(max_length=255, default="")  # Default value is an empty string
    url = models.URLField(max_length=255)
    api_key = models.TextField(max_length=500)

    def __str__(self):
        return self.tenant