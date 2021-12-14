from django.db import models
from accounts.models import User
from django.conf import settings  
# Create your models here.

class Container(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=False, 
        primary_key=True,
    )

    username = models.CharField(
        null= True,
        max_length=30,
    )

    osname = models.CharField(
        null= True,
        max_length=30,
    )

    flag = models.BooleanField(
        'flag',
        default=False,
    )

    ipaddr = models.CharField(
        'container ip address',
        max_length=30,
        blank=True,
        default=None,
        null=True,
    )
    def __str__(self):
        return self.user.uos_id