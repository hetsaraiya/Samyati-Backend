# Generated by Django 5.0.6 on 2024-06-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_privacypolicy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypolicy',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
