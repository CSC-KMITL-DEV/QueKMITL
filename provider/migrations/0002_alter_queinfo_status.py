# Generated by Django 3.2.3 on 2021-06-05 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queinfo',
            name='status',
            field=models.BooleanField(null=True),
        ),
    ]
