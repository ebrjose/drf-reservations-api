# Generated by Django 3.2.9 on 2022-02-22 20:31

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRoom',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Deleted')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Created Date')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Updated Date')),
                ('deleted_date', models.DateField(blank=True, editable=False, verbose_name='Deleted Date')),
                ('type', models.CharField(choices=[('SIMPLE', 'Simple'), ('DOUBLE', 'Double'), ('SUITE', 'Suite')], max_length=10, verbose_name='Room Type')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.PositiveIntegerField(default=10, verbose_name='Price per night')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Room',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Deleted')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Updated Date')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Deleted Date')),
                ('type', models.CharField(choices=[('SIMPLE', 'Simple'), ('DOUBLE', 'Double'), ('SUITE', 'Suite')], max_length=10, verbose_name='Room Type')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.PositiveIntegerField(default=10, verbose_name='Price per night')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
    ]