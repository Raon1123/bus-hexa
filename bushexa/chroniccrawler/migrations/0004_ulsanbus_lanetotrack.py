# Generated by Django 3.2.7 on 2021-10-06 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chroniccrawler', '0003_posofbus'),
    ]

    operations = [
        migrations.CreateModel(
            name='UlsanBus_LaneToTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_id', models.CharField(max_length=20)),
                ('route_num', models.CharField(max_length=20)),
                ('route_direction', models.IntegerField()),
                ('route_class', models.IntegerField()),
                ('route_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chroniccrawler.lanetotrack')),
            ],
        ),
    ]
