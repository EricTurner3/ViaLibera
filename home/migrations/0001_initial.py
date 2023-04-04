# Generated by Django 4.2 on 2023-04-04 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('license', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('make', models.CharField(choices=[('Abarth', 'Abarth'), ('AR', 'Alfa Romeo'), ('AM', 'Aston Martin'), ('Audi', 'Audi'), ('Bentley', 'Bentley'), ('BMW', 'BMW'), ('Bugatti', 'Bugatti'), ('Cadillac', 'Cadillac'), ('Chevrolet', 'Chevrolet'), ('Chrysler', 'Chrysler'), ('Citroen', 'Citroën'), ('Dacia', 'Dacia'), ('Daewoo', 'Daewoo'), ('Daihatsu', 'Daihatsu'), ('Dodge', 'Dodge'), ('Donkervoort', 'Donkervoort'), ('DS', 'DS'), ('Ferrari', 'Ferrari'), ('Fiat', 'Fiat'), ('Fisker', 'Fisker'), ('Ford', 'Ford'), ('Honda', 'Honda'), ('Hummer', 'Hummer'), ('Hyundai', 'Hyundai'), ('Infiniti', 'Infiniti'), ('Iveco', 'Iveco'), ('Jaguar', 'Jaguar'), ('Jeep', 'Jeep'), ('Kia', 'Kia'), ('KTM', 'KTM'), ('Lada', 'Lada'), ('Lamborghini', 'Lamborghini'), ('Lancia', 'Lancia'), ('Land Rover', 'Land Rover'), ('Landwind', 'Landwind'), ('Lexus', 'Lexus'), ('Lotus', 'Lotus'), ('Maserati', 'Maserati'), ('Maybach', 'Maybach'), ('Mazda', 'Mazda'), ('McLaren', 'McLaren'), ('MB', 'Mercedes-Benz'), ('MG', 'MG'), ('Mini', 'Mini'), ('Mitsubishi', 'Mitsubishi'), ('Morgan', 'Morgan'), ('Nissan', 'Nissan'), ('Opel', 'Opel'), ('Peugeot', 'Peugeot'), ('Porsche', 'Porsche'), ('Renault', 'Renault'), ('RR', 'Rolls-Royce'), ('Rover', 'Rover'), ('Saab', 'Saab'), ('Seat', 'Seat'), ('Skoda', 'Skoda'), ('Smart', 'Smart'), ('SsangYong', 'SsangYong'), ('Subaru', 'Subaru'), ('Suzuki', 'Suzuki'), ('Tesla', 'Tesla'), ('Toyota', 'Toyota'), ('Volkswagen', 'Volkswagen'), ('Volvo', 'Volvo')], default='Abarth', max_length=25)),
                ('model', models.CharField(max_length=100)),
                ('vin', models.CharField(max_length=18)),
                ('nickname', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='images/vehicles/')),
                ('primary_driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.person')),
            ],
        ),
    ]