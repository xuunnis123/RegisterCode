from django.db import models
from django.urls import reverse
# Create your models here.
class Code(models.Model):
    user=models.CharField(max_length=264,unique=True)
    code=models.CharField(max_length=264)
    validate=models.DateField()
    mac_address=models.CharField(max_length=264,unique=True)

    def __str__(self):
        return str(self.user)+str(":")+str(self.code)
    
    def get_absolute_url(self):
        return reverse("manage_app:detail", kwargs={"pk": self.pk})