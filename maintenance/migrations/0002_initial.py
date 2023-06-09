# Generated by Django 4.2 on 2023-04-07 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.log'),
        ),
        migrations.AddField(
            model_name='service',
            name='maintenance_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maintenance.maintenance'),
        ),
    ]
