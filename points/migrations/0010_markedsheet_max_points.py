# Generated by Django 4.0.6 on 2024-05-16 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0009_group_use_generic_sheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='markedsheet',
            name='max_points',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
