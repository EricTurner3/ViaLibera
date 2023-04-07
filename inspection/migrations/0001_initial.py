# Generated by Django 4.2 on 2023-04-07 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField()),
                ('inspector_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.person')),
            ],
        ),
        migrations.CreateModel(
            name='InspectionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=25)),
                ('category_desc', models.CharField(default=None, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Inspection Categories',
            },
        ),
        migrations.CreateModel(
            name='InspectionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('desc', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=7)),
                ('index', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Inspection Statuses',
            },
        ),
        migrations.CreateModel(
            name='InspectionTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc_simple', models.CharField(max_length=255)),
                ('desc_detailed', models.TextField()),
                ('unit', models.CharField(max_length=10)),
                ('has_status', models.BooleanField(default=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.inspectioncategory')),
            ],
        ),
        migrations.CreateModel(
            name='InspectionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50)),
                ('skipped', models.BooleanField(default=False)),
                ('notes', models.TextField()),
                ('inspection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.inspection')),
                ('status_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inspection.inspectionstatus')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.inspectiontask')),
            ],
        ),
    ]
