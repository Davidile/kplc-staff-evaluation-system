# Generated by Django 5.0.2 on 2024-07-29 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]