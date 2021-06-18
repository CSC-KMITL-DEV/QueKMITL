# Generated by Django 3.2.3 on 2021-06-16 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_in_type_table'),
        ('provider', '0001_initial'),
        ('booking', '0003_que_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='que_booking',
            name='status',
            field=models.CharField(choices=[('1', 'wait'), ('2', 'put off'), ('3', 'cancel'), ('4', 'delete'), ('5', 'using')], default='1', max_length=2),
        ),
        migrations.CreateModel(
            name='Que_walkin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('1', 'wait'), ('2', 'put off'), ('3', 'cancel'), ('4', 'delete'), ('5', 'using')], default='1', max_length=2)),
                ('que_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.queinfo')),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user_in_type')),
            ],
            options={
                'db_table': 'que_walkin',
                'managed': True,
            },
        ),
    ]
