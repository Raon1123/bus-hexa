# Generated by Django 3.2.7 on 2021-09-20 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_bustimetable_bus_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArrivalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_id', models.IntegerField(default=196040234)),
                ('vehicle_no', models.CharField(max_length=16)),
                ('route_id', models.IntegerField(default=9999)),
                ('remain_time', models.IntegerField(default=9999)),
                ('stop_cnt', models.IntegerField(default=9999)),
                ('stop_name', models.CharField(max_length=128)),
            ],
        ),
    ]
