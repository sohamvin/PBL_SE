# Generated by Django 4.2.10 on 2024-04-13 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_request_final_aprove_date_alter_request_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmap',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('UNDER_REVIEW', 'UNDER_REVIEW'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=50, verbose_name='Status'),
        ),
    ]
