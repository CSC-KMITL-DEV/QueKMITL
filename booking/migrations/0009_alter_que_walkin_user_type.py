# Generated by Django 3.2.3 on 2021-06-18 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
        ('booking', '0008_alter_que_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='que_walkin',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.typeuser'),
        ),
    ]
