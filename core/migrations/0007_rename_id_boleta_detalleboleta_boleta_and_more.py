# Generated by Django 4.0.5 on 2023-05-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_producto_codigo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalleboleta',
            old_name='id_boleta',
            new_name='boleta',
        ),
        migrations.AlterField(
            model_name='detalleboleta',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
