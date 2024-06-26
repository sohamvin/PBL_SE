# Generated by Django 4.2.10 on 2024-04-13 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('role', models.CharField(choices=[('HOD_ENTC', 'HOD_ENTC'), ('HOD_CE', 'HOD_CE'), ('HOD_IT', 'HOD_IT'), ('PRINCIPAL', 'PRINCIPAL'), ('DIRECTOR', 'DIRECTOR'), ('CO-ORDINATOR', 'CO-ORDINATOR'), ('PE_TEACHER', 'PE_TEACHER')], max_length=50, verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Administrator',
                'verbose_name_plural': 'Administrators',
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Club Name')),
                ('club_url', models.URLField(verbose_name='Club Logo URL')),
                ('club_head', models.CharField(blank=True, max_length=50, verbose_name='Club Head')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Club',
                'verbose_name_plural': 'Clubs',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='Event Name')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('description', models.TextField()),
                ('request_id', models.CharField(default='00000000', max_length=8, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.club')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.CharField(default='00000000', max_length=8, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('subject', models.TextField(verbose_name='Subject')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('UNDER_REVIEW', 'UNDER_REVIEW'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=50, verbose_name='Status')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.club', verbose_name='Club')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.event', verbose_name='Event')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
        ),
        migrations.CreateModel(
            name='ReviewMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.administrator', verbose_name='Administrator')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.request', verbose_name='Request')),
            ],
            options={
                'verbose_name': 'Review Message',
                'verbose_name_plural': 'Review Messages',
            },
        ),
        migrations.CreateModel(
            name='RequestMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.request', verbose_name='')),
                ('sendto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.administrator', verbose_name='')),
            ],
            options={
                'verbose_name': 'RequestMap',
                'verbose_name_plural': 'RequestMaps',
            },
        ),
        migrations.AddField(
            model_name='administrator',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.club'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
