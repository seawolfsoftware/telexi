
from django.db import models


class Subscribers(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    conf_num = models.CharField(default='123456789012345', max_length=15)
    confirmed = models.BooleanField(default=False)
