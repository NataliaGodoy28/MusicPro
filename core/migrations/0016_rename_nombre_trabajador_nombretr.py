# Generated by Django 4.2 on 2023-07-04 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_trabajador'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trabajador',
            old_name='nombre',
            new_name='nombretr',
        ),
    ]
