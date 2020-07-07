from django.db import models

# Create your models here.

class CricApi(models.Model):
    UniqueId = models.IntegerField()

   

    class Meta:
        verbose_name_plural = 'UniqueIds'
    
