# Generated by Django 3.2.3 on 2021-06-16 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provider', '0001_initial'),
        ('user', '0003_alter_user_in_type_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0002_delete_user_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Que_booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=10)),
                ('que_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.queinfo')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user_in_type')),
            ],
            options={
                'db_table': 'que_booking',
                'managed': True,
            },
        ),
    ]
