# Generated by Django 4.0.4 on 2023-02-06 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todotask_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todotask',
            name='created_date',
        ),
    ]
