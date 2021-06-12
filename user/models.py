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
        