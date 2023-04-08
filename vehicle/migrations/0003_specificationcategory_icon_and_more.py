# Generated by Django 4.2 on 2023-04-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_alter_vehicle_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificationcategory',
            name='icon',
            field=models.CharField(default='fas fa-star', max_length=50),
        ),
        migrations.AddField(
            model_name='specificationcategory',
            name='order',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
