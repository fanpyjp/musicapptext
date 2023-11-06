from django.db import models

# Create your models here.
class User(models.Model):
    User_id = models.AutoField(auto_created=True,primary_key=True)
    User_name = models.CharField(max_length=20,unique=True)
    Password = models.IntegerField(max_length=30)
    collect = models.ManyToManyField('Music')

class MusicType(models.Model):
    type_id = models.AutoField(auto_created=True,primary_key=True)
    type_name = models.CharField(max_length=30)


class Music(models.Model):
    music_id = models.AutoField(auto_created=True,primary_key=True)
    music_name = models.CharField(max_length=30)
    singer = models.CharField(max_length=30)
    longtime = models.DurationField()
    description = models.TextField(null=True,blank=True)
    music_type = models.ForeignKey(MusicType,on_delete=models.PROTECT)

