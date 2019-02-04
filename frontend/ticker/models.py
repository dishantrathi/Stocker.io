from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.
class StockList(models.Model):
    stock_id = models.SlugField(primary_key=True)
    name = models.TextField(max_length=120)
    count = models.PositiveIntegerField()
    class Meta:
        ordering = ('stock_id',) #helps in alphabetical listing. Sould be a tuple
        
    def __str__(self):
        return self.stock_id+" : "+self.name