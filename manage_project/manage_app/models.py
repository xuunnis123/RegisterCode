from django.db import models

# Create your models here.
class Code(models.Model):
    user=models.CharField(max_length=264,unique=True)
    code=models.CharField(max_length=264,unique=True)
    validate=models.DateField()
    mac_address=models.CharField(max_length=264,unique=True)

    def __str__(self):
        return str(self.user)+str(":")+str(self.code)