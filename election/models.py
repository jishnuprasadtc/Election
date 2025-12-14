from django.db import models
from django.contrib.auth.models import User
from django.db.models import AutoField
from django.db.models import BigAutoField

# Create your models here.

class Election(models.Model):
    name=models.CharField(max_length=200)
    start_date=models.DateTimeField(null=True,blank=True)
    end_date=models.DateTimeField(null=True,blank=True)
    active=models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Position(models.Model):
    election=models.ForeignKey(Election,on_delete=models.CASCADE,null=True,blank=True,related_name='positions')
    name=models.CharField(max_length=200)


    def __str__(self):
        return self.name
    
class Candidates(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='candidacies')
    position=models.ForeignKey(Position,on_delete=models.CASCADE,null=True,blank=True,related_name='candidacies')
    manifesto = models.TextField(blank=True)  #Just cadinate to tell

    class Meta:
        unique_together = ['user']

    def __str__(self):
        return f"{self.user.username}" - { self.position.name}
    

class Vote(models.Model):
    voter=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='vote')
    position=models.ForeignKey(Position,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='vote')
    candiate=models.ForeignKey(Candidates,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='vote')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('voter','position')


    def __str__(self):
        return f"{self.voter.username} -> {self.candidate.user.username} ({self.position.name})" 