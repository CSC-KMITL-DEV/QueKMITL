from django.db import models
from django.contrib.auth.models import User
from provider.models import QueInfo
# Create your models here.

# class User_booking(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     que_id = models.ForeignKey(QueInfo, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=10)
#     class Meta:
#         managed = True
#         db_table = "User_booking"