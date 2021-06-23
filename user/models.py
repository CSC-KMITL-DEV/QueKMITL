from django.db import models
from django.contrib.auth.models import User
from provider.models import TypeUser

# Create your models here.

class User_in_type(models.Model):
    user_type = models.ForeignKey(TypeUser, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "User_in_type"


class User_punish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    punish = models.IntegerField(default=0)
    class Meta:
        managed = True
        db_table = "User_punish"