# Generated by Django 5.1.6 on 2025-05-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_profile_city_remove_profile_door_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='study_year',
            field=models.CharField(blank=True, choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')], max_length=1, null=True),
        ),
    ]
