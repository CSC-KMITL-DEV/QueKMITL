from django.db import models
from django.contrib.auth.models import User
from provider.models import QueInfo,TypeUser
from user.models import User_in_type
# Create your models here.

class Que_booking(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    que_id = models.ForeignKey(QueInfo, on_delete=models.CASCADE)
    user_type = models.ForeignKey(User_in_type, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    rang = models.IntegerField()

    WAIT = '1'
    CANCEL = '2'
    DELETE = '3'
    USING = '4'
    DONE = '5'

    TYPES = (
        (WAIT, 'wait'),
        (CANCEL, 'cancel'),
        (DELETE, 'delete'),
        (USING, 'using'),
        (DONE, 'done'),
    )

    status = models.CharField(max_length=2, choices=TYPES, default='1')
    class Meta:
        managed = True
        db_table = "que_booking"

class Que_walkin(models.Model):
    id = models.AutoField(primary_key=True)
    que_id = models.ForeignKey(QueInfo, on_delete=models.CASCADE)
    user_type = models.ForeignKey(TypeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    rang = models.IntegerField()

    WAIT = '1'
    DELETE = '2'
    USING = '3'
    DONE = '4'
    TYPES = (
        (WAIT, 'wait'),
        (DELETE, 'delete'),
        (USING, 'using'),
        (DONE, 'done'),

    )

    status = models.CharField(max_length=2, choices=TYPES, default='1')
    class Meta:
        managed = True
        db_table = "que_walkin"