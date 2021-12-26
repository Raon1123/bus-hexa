# Generated by Django 3.2.7 on 2021-10-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LaneToTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_name', models.CharField(max_length=30)),
                ('route_id', models.CharField(max_length=20)),
                ('city_code', models.CharField(max_length=10)),
            ],
        ),
    ]
