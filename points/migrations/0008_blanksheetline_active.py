# Generated by Django 4.0.6 on 2024-03-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0007_blanksheetline_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='blanksheetline',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
