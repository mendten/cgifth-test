# Generated by Django 4.0.6 on 2024-03-17 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0005_blanksheetline_group_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blanksheetline',
            name='group_type',
            field=models.CharField(choices=[('bunk', 'bunk'), ('learning_class', 'learning_class'), ('camper', 'camper')], default='bunk', max_length=30),
        ),
    ]
