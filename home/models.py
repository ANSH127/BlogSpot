from django.db import models

# Create your models here.
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=13)
    email=models.CharField(max_length=50)
    desc=models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message From '+self.name+'  Email '+self.email