from django.db import models

# Create your models here.

class TypeUser(models.Model):
    id = models.AutoField(primary_key=True)
    name_type_user = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = "type_user"

class Week_Day(models.Model):
    id = models.AutoField(primary_key=True)
    name_day = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = "week_day"

class TypeQue(models.Model):
    id = models.AutoField(primary_key=True)
    name_type_que = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = "type_que"

class QueInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name_que = models.CharField(max_length=50)
    prefix = models.CharField(max_length=2)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    time_start = models.TimeField()
    time_end = models.TimeField()
    day_open = models.ManyToManyField(Week_Day)
    wait_time = models.IntegerField()
    type_que = models.ManyToManyField(TypeQue)
    type_user = models.ManyToManyField(TypeUser)
    status = models.BooleanField(default=True)
    class Meta:
        managed = True
        db_table = "queinfo"

