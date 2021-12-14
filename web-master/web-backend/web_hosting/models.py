from django.db import models
from datetime import datetime
import pytz # $ pip install pytz
from django.conf import settings  
from pytz import timezone

from accounts.models import User

# Create your models here.
def get_path(instance, filename):
    return '{0}/{1}'.format(instance.sid, filename)


class File(models.Model):
   
    sid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False, 
    )

    file = models.FileField(upload_to=get_path)
    날짜 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)