# Generated by Django 4.0.4 on 2022-05-02 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gemplanner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
