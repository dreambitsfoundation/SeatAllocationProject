# Generated by Django 3.2.12 on 2022-03-08 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='room',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.room'),
        ),
        migrations.CreateModel(
            name='SeatAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_allocation', models.DateField(auto_now_add=True)),
                ('date_of_withhold', models.DateField(null=True)),
                ('seat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.seat')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.student')),
            ],
        ),
    ]