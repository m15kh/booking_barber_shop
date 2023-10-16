# Generated by Django 4.0 on 2023-10-15 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('middle_name', models.CharField(max_length=20)),
                ('specialty', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='YYYY-MM-DD')),
                ('timeslot', models.IntegerField(choices=[(0, '09:00 – 09:30'), (1, '10:00 – 10:30'), (2, '11:00 – 11:30'), (3, '12:00 – 12:30'), (4, '13:00 – 13:30'), (5, '14:00 – 14:30'), (6, '15:00 – 15:30'), (7, '16:00 – 16:30'), (8, '17:00 – 17:30'), (9, '18:00 – 18:30'), (10, '19:00 – 19:30'), (11, '20:00 – 20:30'), (12, '21:00 – 21:30')])),
                ('patient_name', models.CharField(max_length=60)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.doctor')),
            ],
            options={
                'unique_together': {('doctor', 'date', 'timeslot')},
            },
        ),
    ]
