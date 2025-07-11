# Generated by Django 4.0.6 on 2024-03-03 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='is_available_to_all',
            new_name='is_generic',
        ),
        migrations.AddField(
            model_name='markedsheetline',
            name='points_type',
            field=models.CharField(choices=[('custom', 'custom'), ('checkbox', 'checkbox')], default='custom', max_length=20),
        ),
        migrations.CreateModel(
            name='BlankSheetLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_generic', models.BooleanField(default=False)),
                ('points_type', models.CharField(choices=[('custom', 'custom'), ('checkbox', 'checkbox')], default='custom', max_length=20)),
                ('sequence', models.IntegerField(default=0)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sheet', to='points.group')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheet', to='points.task')),
            ],
        ),
    ]
