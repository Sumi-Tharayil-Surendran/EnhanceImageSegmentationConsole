# Generated by Django 4.2.3 on 2023-08-13 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0014_alter_customuser_reset_try'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=200, null=True, verbose_name='skill')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='CreatedDate')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='candidate')),
            ],
        ),
    ]